from functools import wraps
from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.models import Date, User
from project.users.forms import UserForm, LoginForm, UserEditForm, UserInfoForm
from project.dates.forms import DateForm
from flask_login import login_user, logout_user, current_user, login_required
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
# from IPython import embed

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/')
def index():
    dates = Date.query.order_by("timestamp desc").limit(25).all()
    return render_template('users/index.html', user=User.query.first(), dates=dates)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm(request.form)
    if form.validate_on_submit():
        try:
            new_user = User(form.data['username'], form.data['email'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            flash(u"Username already taken.", 'error')
            return render_template('users/signup.html', form=form)
        flash(u"User created! Welcome.", 'positive')
        return redirect(url_for('users.show', id=new_user.id))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            login_user(user)
            flash(u"You have successfully logged in!", 'positive')
            return redirect(url_for('root'))
        flash(u"Invalid credentials.", 'warning')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"You have been signed out.", 'positive')
    return redirect(url_for('users.login'))

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    form = UserEditForm()
    return render_template('users/edit.html', user=User.query.get(id), form=form)

@users_blueprint.route('/<int:id>', methods = ["GET", "PATCH", "DELETE"])
@login_required
@ensure_correct_user
def show(id):
    found_user = User.query.get(id)
    if request.method == 'GET' or current_user.is_anonymous or current_user.get_id() != str(id):
        return render_template('users/show.html', user=found_user, dates=Date.query.filter_by(user_id=id).order_by("timestamp desc"))
    if current_user.is_authenticated and request.method == b"PATCH":
        form = UserEditForm(request.form)
        if form.validate():
            found_user.username = form.data['username']
            if bcrypt.check_password_hash(found_user.password, form.data['old_password']):
                if form.data['new_password'] == form.data['confirm']:
                    found_user.password = bcrypt.generate_password_hash(form.data['new_password']).decode('UTF-8')
                    db.session.add(found_user)
                    db.session.commit()
                    flash(u"User edited!", 'info')
                return redirect(url_for('users.show', id=found_user.id))
            flash(u"User not edited! Double check passwords.", 'warning')
        return render_template('users/edit.html', user=found_user, form=form)
    if current_user.is_authenticated and request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        flash(u"User deleted.", 'info')
        return redirect(url_for('users.signup'))

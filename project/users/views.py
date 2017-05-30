from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.models import Date, User
from project.users.forms import UserEditForm
from project.dates.forms import DateForm
from flask_login import current_user, login_required
from functools import wraps
from project import db
from IPython import embed

from sqlalchemy.exc import IntegrityError

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
  return render_template('users/index.html', user=User.query.first())

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
  form = UserForm(request.form)
  if form.validate_on_submit():
    try:
      new_user = User(form.data['username'], form.data['email'], form.data['password'])
      db.session.add(new_user)
      db.session.commit()
    except IntegrityError as e:
      flash("Username already taken.")
      return render_template('users/signup.html', form=form)
    flash("User created! Welcome.")
    return redirect(url_for('users.show', id=new_user.id))
  return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.data['username']).first()
    if user and bcrypt.check_password_hash(user.password, form.data['password']):
      flash("You have successfully logged in!")
      login_user(user)
      return redirect(url_for('root'))
    flash("Invalid credentials.")
  return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been signed out.')
  return redirect(url_for('users.login'))

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
  form = UserEditForm()
  return render_template('users/edit.html', user=User.query.get(id), form=form)

@users_blueprint.route('/<int:id>', methods =["GET", "PATCH", "DELETE"])
@login_required
@ensure_correct_user
def show(id):
  found_user = User.query.get(id)
  if request.method == 'GET' or current_user.is_anonymous or current_user.get_id() != str(id):
    return render_template('users/show.html', user=found_user)
  if current_user.is_authenticated and request.method == b"PATCH":
    form = UserEditForm(request.form)
    if form.validate():
      found_user.username = form.data['username']
      if bcrypt.check_password_hash(found_user.password, form.data['old_password']):
        if form.data['new_password'] == form.data['confirm']:
          found_user.password = bcrypt.generate_password_hash(form.data['new_password']).decode('UTF-8')
          db.session.add(found_user)
          db.session.commit()
          flash('User edited!')
        return redirect(url_for('users.show', id=found_user.id))
      flash('User not edited! Double check passwords.')
    return render_template('users/edit.html', user=found_user, form=form)
  if current_user.is_authenticated and request.method == b"DELETE":
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for('users.signup'))
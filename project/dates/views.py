from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.models import User, Date, Color
from project.users.views import ensure_correct_user
from project.dates.forms import DateForm
from flask_login import current_user, login_required
from project import db
from datetime import datetime
# from IPython import embed

dates_blueprint = Blueprint(
    'dates',
    __name__,
    template_folder='templates'
)

@dates_blueprint.route('/', methods=["POST"])
@login_required
@ensure_correct_user
def index(id):
    if current_user.get_id() == str(id):
        form = DateForm()
        if form.validate():
            new_date = Date(
                weather=form.weather.data
            )
            db.session.add(new_date)
            db.session.commit()
            flash(u"Date was created.", 'positive')
        return redirect(url_for('dates.show', id=id, date_id=new_date.id))
    return render_template('dates/new.html', form=form)

@dates_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(id):
    return render_template('dates/new.html', form=DateForm(), id=id)

@dates_blueprint.route('/<int:date_id>', methods =["GET", "PATCH", "DELETE"])
@login_required
@ensure_correct_user
def show(id, date_id):
    found_date = Date.query.get_or_404(date_id)
    if request.method == b'PATCH' and current_user.id == id:
        form = DateForm(request.form)
        if form.validate():
            found_date.weather = form.weather.data
            found_date.timestamp = datetime.utcnow()
            db.session.add(found_date)
            db.session.commit()
            flash(u"Date edited!", 'info')
            return redirect(url_for('dates.show', id=id, date_id=found_date.id))
        flash(u"Form not validated. Please try again.", 'warning')
        return render_template('dates/edit.html', date=found_date, form=form)
    if request.method == b"DELETE" and current_user.id == id:
        db.session.delete(found_date)
        db.session.commit()
        flash(u"Date deleted", 'info')
        return redirect(url_for('root'))
    return render_template('dates/show.html', date=found_date)

@dates_blueprint.route('/<int:date_id>/edit')
@login_required
@ensure_correct_user
def edit(id, date_id):
    found_date = Date.query.get_or_404(date_id)
    if current_user.id == id:
        form = DateForm(obj=found_date)
        return render_template('dates/edit.html', date=found_date, form=form)
    else:
        flash(u"You do not have permission to edit.", 'error')
        return redirect(url_for('root'))

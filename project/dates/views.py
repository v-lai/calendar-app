from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.models import User, Date
from project.users.views import ensure_correct_user
from project.dates.forms import DateForm
from flask_login import current_user, login_required
from project import db
from IPython import embed

dates_blueprint = Blueprint(
  'dates',
  __name__,
  template_folder='templates'
)

@dates_blueprint.route('/', methods=["POST"])
def index(id):
  if current_user.get_id() == str(id):
    form = DateForm()
    if form.validate():
      new_date = Date(
        mood=form.mood.data,
        user_id=id
      )
      db.session.add(new_date)
      db.session.commit()
      return redirect(url_for('users.show', id=id))
  return render_template('dates/new.html', form=form)

@dates_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(id):
  return render_template('dates/new.html', form=DateForm(), user_id=id)

@dates_blueprint.route('/<int:date_id>', methods =["GET", "DELETE"])
def show(id, date_id):
  found_date = Date.query.get(date_id)
  if request.method == b"DELETE" and current_user.get_id() == id:
    db.session.delete(found_date)
    db.session.commit()
    return redirect(url_for('dates.index', id=id))
  return render_template('dates/show.html', date=found_date)

from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from project.models import Color

class MultiCheckboxField(SelectMultipleField):
  widget = widgets.ListWidget(prefix_label=False)
  option_widget = widgets.CheckboxInput()

class DateForm(FlaskForm):
  moods = MultiCheckboxField('Moods', coerce=int)

  def set_choices(self):
    self.moods.choices = [(m.id, m.name) for m in Mood.query.all()]

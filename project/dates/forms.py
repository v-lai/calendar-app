from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired
from project.models import Color

class DateForm(FlaskForm):
    weather = RadioField('weather', choices=[('sunny', 'sunny'),
                                             ('cloudy', 'cloudy'),
                                             ('rainy', 'rainy'),
                                             ('snowy', 'snowy'),
                                             ('windy', 'windy'),
                                             ('foggy', 'foggy')])

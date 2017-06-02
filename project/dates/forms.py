from flask_wtf import FlaskForm
from wtforms import RadioField, TextField
from wtforms.validators import DataRequired
from colour import Color

class DateForm(FlaskForm):
    weather = RadioField('weather', choices=[('sunny', 'sunny'),
                                             ('cloudy', 'cloudy'),
                                             ('rainy', 'rainy'),
                                             ('snowy', 'snowy'),
                                             ('windy', 'windy'),
                                             ('foggy', 'foggy')])
    mood = RadioField('mood', choices=[('anticipation', 'anticipation'),
                                          ('joy', 'joy'),
                                          ('anger', 'anger'),
                                          ('surprise', 'surprise'),
                                          ('fear', 'fear'),
                                          ('sadness', 'sadness'),
                                          ('disgust', 'disgust'),
                                          ('acceptance', 'acceptance'),
                                          ('overwhelmed', 'overwhelmed'),
                                          ('empty', 'empty'),
                                          ('appreciated', 'appreciated')])
    color = TextField(Color())
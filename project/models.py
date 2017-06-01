from datetime import datetime
from project import db, bcrypt
from flask_login import UserMixin
from colour import Color
from sqlalchemy_utils import ColorType

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    dates = db.relationship("Date", backref=db.backref('users'), lazy='dynamic')
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)

    def __init__(self, username, email, password, age=None, gender=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.age = age
        self.gender = gender

    def __repr__(self):
        return "User #{}: {}".format(self.id, self.username)


class Date(db.Model):
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    weather = db.Column(db.Text)
    mood = db.Column(db.Text)
    color = db.Column(ColorType)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, weather, mood, color, user_id, timestamp=datetime.utcnow()):
        self.timestamp = timestamp
        self.weather = weather
        self.mood = mood
        self.color = color
        self.user_id = user_id

    def __repr__(self):
        return "Timestamp at {}, weather: {}, mood: {}".format(self.timestamp, self.weather, self.mood)

from datetime import datetime
from project import db, bcrypt
from flask_login import UserMixin

UserDate = db.Table('user_date',
                    db.Column('id',
                              db.Integer,
                              primary_key=True),
                    db.Column('user_id',
                              db.Integer,
                              db.ForeignKey('users.id', ondelete="cascade")),
                    db.Column('date_id',
                              db.Integer,
                              db.ForeignKey('dates.id', ondelete="cascade")))

UserColor = db.Table('user_color',
                     db.Column('id',
                               db.Integer,
                               primary_key=True),
                     db.Column('user_id',
                               db.Integer,
                               db.ForeignKey('users.id', ondelete="cascade")),
                     db.Column('color_id',
                               db.Integer,
                               db.ForeignKey('colors.id', ondelete="cascade")))

DateColor = db.Table('date_color',
                     db.Column('id',
                               db.Integer,
                               primary_key=True),
                     db.Column('date_id',
                               db.Integer,
                               db.ForeignKey('dates.id', ondelete="cascade")),
                     db.Column('color_id',
                               db.Integer,
                               db.ForeignKey('colors.id', ondelete="cascade")))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    dates = db.relationship("Date", secondary=UserDate,
                            backref=db.backref('users'))
    colors = db.relationship("Color", secondary=UserColor,
                             backref=db.backref('users'))
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
    all_users = db.relationship("User", viewonly=True, passive_deletes=True, secondary=UserDate, lazy="joined")
    all_colors = db.relationship("Color", viewonly=True, passive_deletes=True, secondary=DateColor, lazy="joined")

    def __init__(self, weather, timestamp=datetime.utcnow()):
        self.timestamp = timestamp
        self.weather = weather

    def __repr__(self):
        return "Timestamp at {}, weather: {}".format(self.timestamp, self.weather)


class Color(db.Model):
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Text)
    mood = db.Column(db.Text)
    all_users = db.relationship("User", viewonly=True, passive_deletes=True, secondary=UserColor, lazy="joined")
    all_dates = db.relationship("Date", viewonly=True, passive_deletes=True, secondary=DateColor, lazy="joined")

    def __init__(self, color, mood):
        self.color = color
        self.mood = mood

    def __repr__(self):
        return "{} is {}".format(self.color, self.mood)

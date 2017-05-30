from project import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True)
  email = db.Column(db.Text, unique=True)
  password = db.Column(db.Text)
  dates = db.relationship('Date', backref='users', lazy='dynamic')

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

  def __repr__(self):
    return "User #{}: {}".format(self.id, self.username)

class Date(db.Model):
  __tablename__ = 'dates'

  id = db.Column(db.Integer, primary_key=True)
  mood = db.Column(db.Text)
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

  def __init__(self, mood, user_id, timestamp=datetime.utcnow()):
    self.mood = mood
    self.user_id = user_id
    self.timestamp = timestamp

  def __repr__(self):
    return "User #{} feels {} at {}".format(self.user_id, self.mood, self.timestamp)

class Mood(db.Model):
  __tablename__ = 'moods'

  id = db.Column(db.Integer, primary_key=True)
  mood = db.Column(db.Text)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
  date_id = db.Column(db.Integer, db.ForeignKey('date.id', ondelete='CASCADE'))

  def __init__(self, mood, user_id, date_id):
    self.mood = mood
    self.user_id = user_id
    self.date_id = date_id


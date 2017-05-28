from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True)
  email = db.Column(db.Text, unique=True)
  location = db.Column(db.Text)
  password = db.Column(db.Text)
  
  def __init__(self, username, email, location, password):
    self.username = username
    self.email = email
    self.location = location or None
    self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

  def __repr__(self):
    return "User #{}: {}".format(self.id, self.username)
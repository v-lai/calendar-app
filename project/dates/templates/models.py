from project import db 
from datetime import datetime

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

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config['SQLALCHEMY_ECHO'] = True
    app.config.from_object('config.DevelopmentConfig')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

login_manager.login_view = "users.login"

from project.users.views import users_blueprint
from project.dates.views import dates_blueprint
from project.models import User, Date 

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(dates_blueprint, url_prefix='/users/<int:id>/dates')

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

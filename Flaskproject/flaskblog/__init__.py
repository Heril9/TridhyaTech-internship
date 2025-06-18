from datetime import datetime, timezone
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '8c64225882cf2ea01891ec74ffd2ec67'   #protect site from modifying cookies and cross site request forgery
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flaskblog import models
from flaskblog import routes

def init_db():
    with app.app_context():  # Push an application context
        db.create_all()
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure Database
app.config['SECRET_KEY'] = '\xb3L\xf4\xe9\xea\xc8\xee*\xf3\xdb\x8d\x9d\xe6\x7f\x0c\x15\x87\x9e%Z^\xef@^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

import models
import views

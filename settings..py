import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment
from flask_login import LoginManager





# Flask instance
app = Flask(__name__)




basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configuration
# app.logger.setLevel(DEBUG)
app.config ['SECRET_KEY'] = '\xe6\xb5V\x95>\x9e_z\xa2k\xedH\x81\xc6\xe7\x96\x9f6\xc7\xf0\xa8\x05o{'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

#Configuration for authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ="login"
login_manager.init_app(app)

moment = Moment(app)
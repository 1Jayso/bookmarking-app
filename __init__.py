import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

#Dataabase Configuration
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermo.db')
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db = SQLAlchemy(app)

#Configuration for authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = "auth.login"

toolbar = DebugToolbarExtension(app)


# Displaying timest
moment = Moment(app)


from .main import main as main_blueprint 
app.register_blueprint(main_blueprint, url_prefix='/')

from .thermos import thermos as thermos_blueprint
app.register_blueprint(thermos_blueprint, url_prefix='/thermos')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix ='/auth')


from my_project import models
from my_project import views
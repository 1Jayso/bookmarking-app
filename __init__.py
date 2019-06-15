# import os
# from datetime import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import login_manager 
# from flask_moment import Moment

# #Dataabase Configuration
# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermo.db')
# app.config['DEBUG'] = True
# db = SQLAlchemy(app)

# #Configuration for authentication
# login_manager = login_manager()
# login_manager.session.protection = 'strong'
# login_manager.init_app(app)

# moment = Moment(app)

# import models
# import views
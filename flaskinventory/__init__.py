from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required,current_user,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
# the toolbar is only enabled in debug mode:
app.debug = True
app.config['SECRET_KEY'] = '323b22caac41acbf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

db = SQLAlchemy(app)

from flaskinventory import routes

db.create_all()
db.session.commit()



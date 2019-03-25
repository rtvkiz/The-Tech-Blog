from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
login_manager=LoginManager(app)
login_manager.login_view='login'
app.config['SECRET_KEY']='1aa34dc967a1993a9e9c932a233a3188'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
from blog import routes
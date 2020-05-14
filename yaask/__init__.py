#!/usr/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_ckeditor import CKEditor, CKEditorField
from os import environ
import os


app = Flask(__name__, template_folder='templates' , static_folder="static")

try:
	app.config.from_object('yaask.config.DevelopmentConfig')
	print ("try")
except:
	print ("except")
	app.config["SECRET_KEY"] = environ['SECRET_KEY']
	app.config["DEBUG"] = True
	app.config["TESTING"] = False
	app.config["SQLALCHEMY_DATABASE_URI"] = environ['DATABASE_URL']
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["WTF_CSRF_SECRET_KEY"] = app.config["SECRET_KEY"]


app.config['CKEDITOR_PKG_TYPE'] = 'basic'
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to view this page'

from yaask import routes

from yaask.users.routes import users
from yaask.tests.routes import tests
from yaask.quest.routes import quest
from yaask.main.routes import main


app.register_blueprint(users)
app.register_blueprint(tests)
app.register_blueprint(quest)
app.register_blueprint(main)
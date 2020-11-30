#!/usr/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_ckeditor import CKEditor, CKEditorField
from os import environ
from flask_mail import Mail
import os


app = Flask(__name__, template_folder='templates' , static_folder="static")

try:
	from yaask.config import MAIL_ID, MAIL_PASSWORD
	app.config.from_object('yaask.config.DevelopmentConfig')
	print ("try")
except:
	print ("except")
	app.config["SECRET_KEY"] = environ['SECRET_KEY']
	app.config["DEBUG"] = True
	app.config["TESTING"] = False
	app.config["SQLALCHEMY_DATABASE_URI"] = environ['DATABASE_URL']
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config.update(dict(
		DEBUG = True,
		MAIL_SERVER = 'smtp.googlemail.com',
		MAIL_PORT = 465,
		MAIL_USE_TLS = False,
		MAIL_USE_SSL = True,
		MAIL_USERNAME = environ['MAIL_ID'],
		MAIL_PASSWORD = environ['MAIL_PASSWORD'],
	))


app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True


mail = Mail(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to view this page'


from yaask.modules.users.routes import users
from yaask.modules.tests.routes import tests
from yaask.modules.quest.routes import quest
from yaask.modules.main.routes import main
from yaask.modules.practice_test.routes import practice

app.register_blueprint(users)
app.register_blueprint(tests)
app.register_blueprint(quest)
app.register_blueprint(main)
app.register_blueprint(practice)
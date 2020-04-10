from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os import environ

from app import app, db

try:
	app.config.from_object('config.DevelopmentConfig')
	print ("try")
except:
	print ("except")
	app.config["SECRET_KEY"] = environ['SECRET_KEY']
	app.config["DEBUG"] = True
	app.config["TESTING"] = False
	app.config["SQLALCHEMY_DATABASE_URI"] = environ['DATABASE_URL']
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["WTF_CSRF_SECRET_KEY"] = app.config["SECRET_KEY"]


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
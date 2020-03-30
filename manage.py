from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app import app, db


try:
	app.config.from_object('config.DevelopmentConfig')
	print ("try")
except:
	print ("except")
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_SECRET_KEY = SECRET_KEY

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
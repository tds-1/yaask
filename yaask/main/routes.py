from flask import Flask, render_template, Blueprint
from yaask import app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in

main = Blueprint('main',__name__)

@main.route('/')
def home():
	return render_template('index.html')

@main.route('/about')
def about():
	return render_template('about.html')


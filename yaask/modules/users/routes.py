from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from passlib.context import CryptContext
from yaask.modules.users.forms import LoginForm, RegisterForm
from yaask.modules.users.auth import OAuthSignIn, GoogleSignIn
import math
from yaask.models import *
from yaask import app

users = Blueprint('users',__name__)

SCHEMES = 'pbkdf2_sha256'
pwd_context = CryptContext(
    schemes=[SCHEMES],
    default=SCHEMES,
    pbkdf2_sha256__default_rounds=30000
    )

secret_key='hello_bhai'


@users.route('/authorize/<provider>')
def oauth_authorize(provider):
	# Flask-Login function
	if not current_user.is_anonymous():
		return redirect(url_for('main.home'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@users.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous():
		return redirect(url_for('main.home'))
	oauth = OAuthSignIn.get_provider(provider)
	name,username,email = oauth.callback()

	if email is None:
	# I need a valid email address for my user identification
		flash('Authentication failed.')
		return redirect(url_for('main.home'))

	# Look if the user already exists
	que=User.query.filter(User.email == email).first()
	email=str(email)
	if( que is None):
		user = User(
			name=name,
			username=username,
			email=email,
			phone_no="",
			password=os.getrandom(10, os.GRND_NONBLOCK),
			role = "student",
			score=0
		)
		db.session.add(user)
		db.session.commit()
	else:
		user=que
	login_user(user)
	return redirect(url_for('main.home'))

@users.route('/login', methods=['GET', 'POST'])
def login():
	error=""
	form = LoginForm(request.form)
	form1 = RegisterForm(request.form)
	if request.method == 'POST':
		try:
			if form.validate_on_submit():
				user = User.query.filter_by(username=request.form['username']).first()
				if user is not None and pwd_context.verify(request.form['password'], user.password) and form.role.data == user.role:
					login_user(user)
					return redirect(url_for('main.home'))
				else:
					error = ' * Invalid Credentials'
			else:
				error = ' * Invalid Credentials'
				return render_template('login.html', form=form, error=error , form1=form1)
			return render_template('login.html', form=form , form1=form1)

		except:
			print (form.validate_on_submit())
			if form.validate_on_submit():
				user = User(
					name=form.name.data,
					username=form.username.data,
					email=form.email.data,
					phone_no=form.phone_no.data,
					password=form.password.data,
					phone_verified=False,
					role= form.role.data,
					score=0
				)
				email_query=User.query.filter(User.email == user.email).first()
				username_query=User.query.filter(User.username == user.username).first()
				if(email_query is not None):
					error=" * email already registered"
					flash (error, 'danger')
					form.password.data=''
					return render_template('login.html', form=form , form1=form1)
				elif(username_query is not None):
					error=" * username already taken"
					flash (error, 'danger')
					form.password.data=''
					return render_template('login.html', form=form , form1=form1)
				else:
					db.session.add(user)
					db.session.commit()
					login_user(user)
					return redirect(url_for('main.home'))

	return render_template('login.html', form=form , form1=form1)




@users.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.home'))

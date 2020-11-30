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
import os
from .utils import generate_confirmation_token, confirm_token, send_email

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
	print ("callback",provider)
	if not current_user.is_anonymous():
		return redirect(url_for('main.home'))
	oauth = OAuthSignIn.get_provider(provider)
	name,username,email,picture = oauth.callback()

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
			email_verified=True,
			phone_no="",
			phone_verified=False,
			password=os.getrandom(10, os.GRND_NONBLOCK),
			role = "student",
			score=0,
			picture= picture
		)
		user.email_verified_on = datetime.datetime.now()
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
		if form.validate_on_submit() != form1.validate_on_submit():
			if form.validate_on_submit():
				user = User.query.filter_by(username=request.form['username']).first()
				if user is not None and pwd_context.verify(request.form['password'], user.password) and form.role.data == user.role:
					login_user(user)
					return redirect(url_for('users.unconfirmed'))
				else:
					error = ' * Invalid Credentials'
					form.password.data=''
					form.username.data=''
					form.role.data=''
					return render_template('login.html', form=form, error=error , form1=form1)
			else:
				error = ' * Invalid Credentials'
				return render_template('login.html', form=form, error=error , form1=form1)
			return render_template('login.html', form=form , form1=form1)

		else:
			if form1.validate_on_submit():
				user = User(
					name=form1.name.data,
					username=form1.username.data,
					email=form1.email.data,
					email_verified=False,
					phone_no=form1.phone_no.data,
					password=form1.password.data,
					phone_verified=False,
					role= form1.role.data,
					score=0,
					picture= ""
				)
				email_query=User.query.filter(User.email == user.email).first()
				username_query=User.query.filter(User.username == user.username).first()
				if(email_query is not None and email_query.email_verified == True):
					error=" * email already registered"
					flash (error, 'danger')
					form1.password.data=''
					return render_template('login.html', form=form , form1=form1)
				elif(username_query is not None):
					error=" * username already taken"
					flash (error, 'danger')
					form1.password.data=''
					return render_template('login.html', form=form , form1=form1)
				else:
					db.session.add(user)
					db.session.commit()
					token = generate_confirmation_token(user.email)
					confirm_url = url_for('users.confirm_email', token=token, _external=True)
					html = render_template('activate.html', confirm_url=confirm_url)
					subject = "Please confirm your email"
					send_email(user.email, subject, html)
					login_user(user)

					flash('A confirmation email has been sent via email.', 'success')
					return redirect(url_for('users.unconfirmed'))

	return render_template('login.html', form=form , form1=form1)

@users.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter(User.email == email).first_or_404()
    if user.email_verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_verified = True
        user.email_verified_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))

@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.email_verified:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')

@users.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('users.unconfirmed'))


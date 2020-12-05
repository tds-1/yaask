from flask_wtf import Form
from wtforms import TextField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.html5 import EmailField
from wtforms import validators


class RegisterForm(Form):
	name = TextField(
		'name',
		validators=[DataRequired()]
	)
	username = TextField(
		'username',
		validators=[DataRequired(), Length(min=3, max=25)]
	)

	email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

	phone_no = TextField(
		'phone number',
		validators=[DataRequired()]
	)
	password = PasswordField(
		'password',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
	confirm = PasswordField(
		'confirm',
		validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
	)

class LoginForm(Form):
	username = TextField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_ckeditor import CKEditor, CKEditorField

class RegisterForm(Form):
	name = TextField(
		'name',
		validators=[DataRequired()]
	)
	username = TextField(
		'username',
		validators=[DataRequired(), Length(min=3, max=25)]
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

class SubmitForm(Form):
	question = CKEditorField('question', validators=[DataRequired()])
	option1 = TextField('option1', validators=[DataRequired()])
	option2 = TextField('option2', validators=[DataRequired()])
	option3 = TextField('option3', validators=[DataRequired()])
	option4 = TextField('option4', validators=[DataRequired()])
	answer = SelectField(
		'answer', 
		choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], 
		validators=[DataRequired()]
	)
	category = SelectField(
		'category', 
		choices=[('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')], 
		validators=[DataRequired()]
	)
	difficulty = SelectField(
		'Difficulty', 
		choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
		validators=[DataRequired()]
	)
	comment = TextField('comment')


class SubmitForm2(Form):
	question1 = CKEditorField('question', validators=[DataRequired()])
	answer1 = FloatField('answer', validators=[DataRequired()])
	category1 = SelectField(
		'category', 
		choices=[('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')], 
		validators=[DataRequired()]
	)
	difficulty1 = SelectField(
		'Difficulty', 
		choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
		validators=[DataRequired()]
	)
	comment1 = TextField('comment')

class QuizForm(Form):
	attempted_answer = SelectField(
		'attempted_answer',
		choices=[('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')],
		validators=[DataRequired()]
	)
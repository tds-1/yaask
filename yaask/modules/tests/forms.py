from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError
from validate_email import validate_email
from datetime import timedelta, datetime
from flask_wtf import FlaskForm


class QuizForm(Form):
	attempted_answer = SelectField(
		'attempted_answer',
		choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
		validators=[DataRequired()]
	)

class GenerateForm(Form):
	name = TextField('name', validators=[DataRequired()])
	time = IntegerField('time', validators=[DataRequired()])
	institution = TextField('institution', validators=[DataRequired()])

class RandomTest(Form):
	subject = SelectField(
		'subject',
		choices=[('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')],
		validators=[DataRequired()]
	)
	number_of_questions = IntegerField(
		'number of questions', validators=[DataRequired()]
	)
	avg_difficulty = SelectField(
		'average difficulty',
		choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
		validators=[DataRequired()]
	)


class UploadForm(FlaskForm):
	subject = TextField('Subject', validators=[DataRequired()])
	topic = TextField('Topic', validators=[DataRequired()])
	start_date = DateField('Start Date', validators=[DataRequired()])
	start_time = TimeField('Start Time', default=datetime.utcnow()+timedelta(hours=5.5), validators=[DataRequired()])
	end_date = DateField('End Date', validators=[DataRequired()])
	end_time = TimeField('End Time', default=datetime.utcnow()+timedelta(hours=6.5), validators=[DataRequired()])
	show_result = BooleanField('Show Result after completion', validators=[DataRequired()])
	neg_mark = BooleanField('Enable negative marking', validators=[DataRequired()])
	duration = TextField('Duration(in min)', validators=[DataRequired()])
	password = TextField('Test Password', validators=[DataRequired()])

	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("End date must not be earlier than start date.")
	
	def validate_end_time(form, field):
		start_date_time = datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		end_date_time = datetime.strptime(str(form.end_date.data) + " " + str(field.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		if start_date_time >= end_date_time:
			raise ValidationError("End date time must not be earlier/equal than start date time")
	
	def validate_start_date(form, field):
		if datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S") < datetime.now():
			raise ValidationError("Start date and time must not be earlier than current")


class TestForm(Form):
	test_id = StringField('Test ID')
	password = StringField('Test Password')

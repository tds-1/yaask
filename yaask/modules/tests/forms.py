from flask_wtf import Form
from wtforms import TextField, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms import validators


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

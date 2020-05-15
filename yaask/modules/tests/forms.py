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


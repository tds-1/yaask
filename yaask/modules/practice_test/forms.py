from flask_wtf import Form
from wtforms import TextField,  SelectField, FloatField, StringField
from wtforms.validators import DataRequired
from wtforms import validators


class PracticeTest(Form):
	subject = SelectField(
		'subject',
		choices=[('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')],
		validators=[DataRequired()]
	)
	topic = SelectField(
		'topic',
		choices=[('Human Health  and Disease', 'Human Health and Disease')],
		validators=[DataRequired()]
	)



class TestForm(Form):
	test_id = StringField('Test ID')
	password = StringField('Test Password')

from flask_wtf import Form
from wtforms import TextField,  SelectField, FloatField, StringField, RadioField
from wtforms.validators import DataRequired
from wtforms import validators


class PracticeTest(Form):
	subject = RadioField(
		'Subject',
		choices=[('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')],
		validators=[DataRequired()]
	)
	f = open("yaask/tag.txt", "r")
	x= (f.read())
	ini=0
	tag=[]
	for i in range (0,len(x)):
		if (x[i]=='\n'):
			tag.append((x[ini:i],x[ini:i]))
			ini=i+1
	tag.append((x[ini:len(x)],x[ini:len(x)]))
	topic = SelectField(
		'Topic', 
		choices=tag,
		validators=[DataRequired()]
	)




class TestForm(Form):
	test_id = StringField('Test ID')
	password = StringField('Test Password')

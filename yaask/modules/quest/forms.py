from flask_wtf import Form
from wtforms import TextField,  SelectField, FloatField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import validators

f = open("yaask/tag.txt", "r")
x= (f.read())
ini=0
tag=[]
tag.append(('all','All Topics'))
for i in range (0,len(x)):
	if (x[i]=='\n'):
		tag.append((x[ini:i],x[ini:i]))
		ini=i+1
tag.append((x[ini:len(x)],x[ini:len(x)]))


class SubmitForm(Form):
	question = CKEditorField('question', validators=[DataRequired()])
	a = TextField('a', validators=[DataRequired()])
	b = TextField('b', validators=[DataRequired()])
	c = TextField('c', validators=[DataRequired()])
	d = TextField('d', validators=[DataRequired()])
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
	tags = SelectField(
		'Tags', 
		choices=tag,
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

class FilterForm(Form):
	subject = SelectField(
		'Subject', 
		choices=[('all','All Subjects'), ('math', 'Math'), ('chemistry', 'Chemistry'), ('physics', 'Physics'), ('biology', 'Biology'), ('other', 'Other')], 
		validators=[DataRequired()]
	)
	tags = SelectField(
		'Topic', 
		choices=tag,
		validators=[DataRequired()]
	)


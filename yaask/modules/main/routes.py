from flask import Flask, render_template, Blueprint, url_for, redirect
from yaask import app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from yaask.models import *

main = Blueprint('main',__name__)

@main.route('/')
def home():
	try:
		current_user.id
		return redirect(url_for('dashboard'))
	except:
		return render_template('index.html')
	

@main.route('/about')
def about():
	return render_template('about.html')

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')



@app.route('/upload')
@login_required
def upload():
	print (current_user.username)
	f1 = open("yaask/answer.txt", "r")
	ans= (f1.read())
	answer = []
	for i in range (0,len(ans)):
		if(ans[i].isdigit() and ans[i+1]==' '):
			answer.append(ans[i+2])
		if(ans[i].isdigit() and ans[i+1].isdigit() and ans[i+1]==' '):
			answer.append(ans[i+3])
	f2 = open("yaask/comment.txt", "r")
	ans= (f2.read())
	comment = []
	l=0
	for i in range (10,len(ans)):
		if(ans[i].isdigit() and ans[i+1]==' ' and ans[i+2]=='('):
			comment.append(ans[l+2:i])
			l = i
		if(ans[i].isdigit() and ans[i+1].isdigit() and ans[i+2]==' ' and ans[i+2]=='('):
			comment.append(ans[l+3:i])
			l = i
	comment.append(ans[l+3:])
	f = open("yaask/question.txt", "r")
	x= (f.read())
	s=[]
	l=2
	for i in range (1,len(x)):
		if((x[i].isdigit() and x[i+1]==' ' and x[i+2].isupper()) ):
			s.append(x[l:i])
			i+=2
			l=i
		elif((x[i].isdigit() and x[i+1].isdigit() and x[i+2]==' ' and x[i+3].isupper())):
			s.append(x[l:i])
			i+=3
			l=i
		elif((x[i].isdigit() and x[i+1].isdigit() and x[i+2].isdigit() and x[i+3]==' ' and x[i+4].isupper())):
			s.append(x[l:i])
			i+=4
			l=i
	s.append(x[l:len(x)])
	#s is full question
	question=[]
	count=0
	co=0
	for y in s:
		br=[]
		l=0
		fl=0
		if (len(y)==0):
			continue
		co+=1
		# print (co,y)
		# print (y)
		for i in range(0,len(y)-3):
			if(y[i]=='\n' and y[i+1]=='A' and y[i+2]==' '):
				br.append(y[l:i])
				l=i+3
				i=i+2
			if(y[i]=='\n' and y[i+1]=='B' and y[i+2]==' '):
				br.append(y[l:i])
				l=i+3
				i=i+2
			if(y[i]=='\n' and y[i+1]=='C' and y[i+2]==' '):
				br.append(y[l:i])
				l=i+3
				i=i+2
			if(y[i]=='\n' and y[i+1]=='D' and y[i+2]==' '):
				br.append(y[l:i])
				l=i+3
				i=i+2
				br.append(y[l:])
				break
		if (len(br)==0):
			continue
		i=br
		comment[count]=comment[count][:-1]
		print (comment[count], br, answer[count], count)
		questiondata = Questions(
			question=i[0],
			a=i[1],
			b=i[2],
			c=i[3],
			d=i[4],
			answer=answer[count].upper(),
			creatorid=current_user.id,
			category='biology',
			difficulty='3',
			question_score=60,
			comment=comment[count],
			tags=['Human Health  and Disease'],
			attempts=50
		)
		db.session.add(questiondata)
		db.session.commit()
		print (questiondata)
		count+=1

	return 'hello world'


# upload()
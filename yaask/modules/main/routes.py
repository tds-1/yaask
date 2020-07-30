from flask import Flask, render_template, Blueprint, url_for, redirect
from yaask import app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from yaask.models import *

main = Blueprint('main',__name__)

@main.route('/')
def home():			
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

	for y in s:
		br=[]
		l=0
		fl=0
		if (len(y)==0):
			continue
		# print (y)
		for i in range(0,len(y)-15):
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
			if(y[i]=='\n' and y[i+1]=='A' and y[i+2]=='n' and y[i+3]=='s' and y[i+4]=='w'):
				br.append(y[l:i])
				br.append(y[i+17:i+18])
				break
		if (len(br)==0):
			continue
		question.append(br)
		i=br
		print (count)
		count+=1

		questiondata = Questions(
			question=i[0],
			a=i[1],
			b=i[2],
			c=i[3],
			d=i[4],
			answer=i[5],
			creatorid=current_user.id,
			category='biology',
			difficulty='1',
			question_score=0,
			comment='',
			tags=[]
		)
		print (questiondata)
		db.session.add(questiondata)
		db.session.commit()


	return 'hello world'


# upload()
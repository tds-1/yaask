#!/usr/bin/python
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from passlib.context import CryptContext
from flask_login import UserMixin
from pickle import loads, dumps
from flask_session import Session
from flask_weasyprint import HTML, render_pdf
import json
import os
from forms import LoginForm, RegisterForm, SubmitForm, QuizForm

#Make the flash for submit() fade slowly so when the next question comes it lights up again

#Create the app and configure it
app = Flask(__name__, template_folder='templates' , static_folder="static")
try:
	app.config.from_object('config.DevelopmentConfig')
	print ("try")
except:
	print ("except")
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_SECRET_KEY = SECRET_KEY

#Create Database object
db = SQLAlchemy(app)

#secret key
secret_key='hello_bhai'

#Create encrypt object
SCHEMES = 'pbkdf2_sha256'

pwd_context = CryptContext(
    schemes=[SCHEMES],
    default=SCHEMES,
    pbkdf2_sha256__default_rounds=30000
    )

#Importing the models after creation of the app
from models import *

#Create instance of LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

#Configuring the login_manager object
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to view this page'

@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.id == int(userid)).first()

def getStandings():
	users = User.query.order_by(User.score.desc())
	return users

@app.route('/')
def home():
	print ("This is the very first page of the yaask application")
	return render_template('hello.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	print ("here we present the login pages")
	logout_user()
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by(username=request.form['username']).first()
			if user is not None and pwd_context.verify(request.form['password'], user.password):
				login_user(user)
				flash('You have been logged in.')
				return redirect(url_for('home'))
			else:
				error = 'Invalid Credentials, try again'
		else:
			error = 'Invalid Credentials, try again'
			render_template('login.html', form=form, error=error)
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User(
				name=form.name.data,
				username=form.username.data,
				password=form.password.data,
				score=0
			)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			flash('You been registered and logged in')
			return redirect(url_for('home'))

	logout_user()
	flash('You have been logged out')
	return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('login'))

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
	form = SubmitForm()
	if form.validate_on_submit():
		questiondata = Questions(
			question=form.question.data,
			option1=form.option1.data,
			option2=form.option2.data,
			option3=form.option3.data,
			option4=form.option4.data,
			answer=form.answer.data,
			creatorid=current_user.id,
			category=form.category.data,
			difficulty=form.difficulty.data,
			question_score=0,
		)
		db.session.add(questiondata)
		db.session.commit()
		flash('Your question has been nestled deep within the quizzing engine')
		return render_template('submit.html', form=form, users=getStandings())
	return render_template('submit.html', form=form, users=getStandings())

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
	form = QuizForm()
	if current_user.answered is None:
		current_user.answered = dumps([])
		db.session.commit()
		questions_to_display = Questions.query.filter().all()
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())

	else:
		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter().all()
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())

@app.route('/answer')
def fetch_answer():
	#id is the question id and userid is the User id
	#Storing the data from the request
	id = request.args.get('id', 0, type=int)
	value = request.args.get('value', 0, type=str)
	userId = request.args.get('userid', 0, type=int)

	#Fetching question and User data
	attempted_question = Questions.query.filter( Questions.questionid == id ).all()
	presentUser = User.query.get( userId )
	presentScore = presentUser.score

	#Appropirately changing the USER's score
	if attempted_question[0].answer == value:
		if attempted_question[0].difficulty == 'easy':
			presentScore = presentScore + 1
		elif attempted_question[0].difficulty == 'moderate':
			presentScore = presentScore + 2
		elif attempted_question[0].difficulty == 'hard':
			presentScore = presentScore + 3
		elif attempted_question[0].difficulty == 'insane':
			presentScore = presentScore + 4		
		
		presentUser.score = presentScore
		correct = 1
	else:
		presentScore = presentScore - 1
		presentUser.score = presentScore
		correct = 0


	beforePickle = current_user.answered
	afterPickle = loads(beforePickle)

	afterPickle.append(id)
	current_user.answered = dumps(afterPickle)
	db.session.commit()

	return jsonify(score = presentScore, correct = correct)


@app.route('/quiz/<string:category>')
@login_required
def categorywise(category):
	categoryList = ['math',
		'chemistry',
		'physics',
		'biology',
		'other',]
	if category in categoryList:
		form = QuizForm()
		if current_user.answered is None:
			current_user.answered = dumps([])
			db.session.commit()

		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter().filter( Questions.category == category ).all()

		if len(questions_to_display) is 0:
			flash("We're so sorry but it seems that there are no questions on this topic")
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())
	else:
		form = QuizForm()
		if current_user.answered is None:
			current_user.answered = dumps([])
			db.session.commit()


		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter().all()
		flash('Please enter a url where the category is any one of' + str(categoryList))
		return redirect(url_for('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings()))

@app.route('/score')
@login_required
def scoreboard():
	#To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
	users = User.query.order_by(User.score.desc())
	return render_template('scoreboard.html', users=users)


@app.route('/test', methods=['GET','POST'])
@login_required
def test():
	categoryList = ['math',
		'chemistry',
		'physics',
		'biology',
		'other',]
	#To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
	if request.method == 'GET':
		db.session.commit()
		questions_to_display = Questions.query.filter().all()
		return render_template('test.html', questions_to_display=questions_to_display, categoryList=categoryList)

	if request.method == 'POST':		
		questions_to_display = Questions.query.filter().all()
		selected=[]
		for question in questions_to_display:
			check=request.form.get(str(question.questionid))
			if check=="checked":
				selected.append(question.questionid)
		
		random_questions=[]
		for category in categoryList:
			n=request.form[category]
			if  len(n)>0:
				temp=Questions.query.filter( ~Questions.questionid.in_(selected)).filter(Questions.category==category).order_by(Questions.question_score).limit(n).all()
				for t in temp:
					selected.append(t)
		
		for question in random_questions:
			print (question.question, question.question_score)
			selected.append(question.questionid)
		
		for question in questions_to_display:
			check=request.form.get(str(question.questionid))
			if check=="checked":
				question.question_score=question.question_score+1
				db.session.commit()
	
		for question in random_questions:
			question.question_score=question.question_score+1
			db.session.commit()
	
		testdata = Test(
			creatorid=current_user.id,
			selected=selected,
		)
		db.session.add(testdata)
		db.session.commit()
		session['selected']=selected
		session['testid']=testdata.testid
		questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
		
		return redirect(url_for('generated_test'))


@app.route('/generated_test', methods=['GET','POST'])
@login_required
def generated_test():
	testid=session.get('testid')
	z=Test.query.filter(Test.testid==testid).one()
	selected=z.selected
	return render_template('chose_test.html',testid=testid)


# @app.route('/online_test', methods=['GET','POST'])
# @login_required
# def print_test():
# 	selected=session.get('selected')
# 	questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
# 	html= render_template("generate.html",questions_to_display=questions_to_display)
# 	return render_pdf(HTML(string=html))

@app.route('/print_test', methods=['GET','POST'])
@login_required
def print_test():
	selected=session.get('selected')
	questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
	html= render_template("generate.html",questions_to_display=questions_to_display)
	return render_pdf(HTML(string=html))

		

#Starting the server with the run method
if __name__ == '__main__':
	app.run()
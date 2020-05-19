from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from flask_session import Session
from flask_weasyprint import HTML, render_pdf
import json
from yaask.modules.tests.forms import  QuizForm, GenerateForm, RandomTest
import math
from yaask.models import *
from yaask import app
from yaask.modules.tests.utils import choosequestions

tests = Blueprint('tests',__name__)

secret_key='hello_bhai'


@app.route('/test', methods=['GET','POST'])
@login_required
def test():
	categoryList = ['math',
		'chemistry',
		'physics',
		'biology',
		'other',]
	#To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
	form=RandomTest()
	
	if request.method == 'GET':
		db.session.commit()
		questions_to_display = Questions.query.filter().all()
		return render_template('test.html',form=form, questions_to_display=questions_to_display, categoryList=categoryList)

	if request.method == 'POST':		
		questions_to_display = Questions.query.filter().all()
		selected=[]
		for question in questions_to_display:
			check=request.form.get(str(question.questionid))
			if check=="checked":
				selected.append(question.questionid)
		
		category=form.subject.data
		avg=form.avg_difficulty.data
		n=form.number_of_questions.data
		
		temp=Questions.query.filter( ~Questions.questionid.in_(selected)).filter(Questions.category==category).all()
		arr=[]
		for x in temp:
			arr.append((int(x.difficulty), x.question_score, x.questionid))
	
		random_questions=choosequestions(arr, avg, n)
		print (random_questions)
		for question in random_questions:
			selected.append(question[2])
		#update score
		questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
		for x in questions_to_display:
			x.question_score=x.question_score+1
			db.session.commit()

		testdata = Test(
			creatorid=current_user.id,
			selected=selected,
		)
		db.session.add(testdata)
		db.session.commit()
		session['selected']=selected
		session['testid']=testdata.testid
		
		return redirect(url_for('generated_test'))



@app.route('/preview-test', methods=['GET','POST'])
@login_required
def preview_test():
	if request.method=='GET':
		id=current_user.id
		test= Test.query.filter(Test.creatorid==id).all()
		return render_template ("preview-test.html",test=test)

	if request.method=='POST':
		print ("post")
		try:
			x=request.form['button']
			session['testid']=x
			return redirect(url_for('generated_test'))

		except:
			x=request.form['delete']
			delet=Test.query.filter(Test.testid==x).one()
			print (delet)
			db.session.delete(delet)
			print ("deleted")
			db.session.commit()
			return redirect(url_for('preview_test'))
		


@app.route('/generated_test', methods=['GET','POST'])
@login_required
def generated_test():
	testid=session.get('testid')
	z=Test.query.filter(Test.testid==testid).one()
	selected=z.selected
	form = GenerateForm()
	return render_template('chose_test.html',testid=testid,form=form)


@app.route('/online_test', methods=['GET','POST'])
@login_required
def online_test():
	if request.method=='GET':
		id=request.args.get('id')
		selected=Test.query.filter(Test.testid==id).one()
		selected=selected.selected
		questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
		return render_template("online_test.html",questions_to_display=questions_to_display,id=id)
	if request.method=='POST':
		id=request.args.get('id')
		selected=Test.query.filter(Test.testid==id).one()
		selected=selected.selected
		print (selected)
		score=0
		questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
		quest={}
		for x in selected:
			x=str(x)
			z=request.form[x]

			answer=Questions.query.filter(Questions.questionid==x).one()
			ans=answer.answer
			
			if ((answer.option1=='-1') and (answer.option2=='-1') and (answer.option3=='-1') and (answer.option4=='-1')):
				try:
					z=str(int(float(z)))
				except:
					z=""
				ans=str(int(float(ans)))
				if(len(z)==0):
					quest[answer]='N'
					pass
				elif (z==ans):
					quest[answer]='C'
					score=score+4
				else:
					quest[answer]='W'
					score=score-1
		
			else:
				if(z=='N'):
					quest[answer]='N'
					pass
				elif (z==ans):
					quest[answer]='C'
					score=score+4
				else:
					quest[answer]='W'
					score=score-1
		
		for x in quest:
			print (x,quest[x])
		return  render_template('result.html',score=score,questions_to_display=quest)

@app.route('/print_test', methods=['GET','POST'])
@login_required
def print_test():
	selected=session.get('selected')
	questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
	form= GenerateForm()
	name=form.name.data.upper()
	time=form.time.data
	institution=form.institution.data.upper()
	html= render_template("generate.html",questions_to_display=questions_to_display,name=name, time=time, institution=institution)
	return render_pdf(HTML(string=html))


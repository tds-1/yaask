from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from flask_session import Session
from flask_weasyprint import HTML, render_pdf
import json
from yaask.tests.forms import  QuizForm, GenerateForm
import math
from yaask.models import *
from yaask import app


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
			# print (n, category)
			if  len(n)>0:
				temp=Questions.query.filter( ~Questions.questionid.in_(selected)).filter(Questions.category==category).order_by(Questions.question_score).limit(n).all()
			# print (selected)
				for t in temp:
					selected.append(t.questionid)
		# print (selected)
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


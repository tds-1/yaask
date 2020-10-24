from flask import Flask, render_template, Blueprint, url_for, redirect, request
from yaask import app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from yaask.models import *
from yaask.modules.practice_test.forms import PracticeTest, TestForm
import pickle
import string
import random
from datetime import timedelta, datetime


practice = Blueprint('practice',__name__)

@practice.route('/practice-test', methods=['GET', 'POST'])
@login_required
def practice_test():
	form = PracticeTest(request.form)
	if request.method == 'POST':
		topic = form.topic.data
		subject = form.subject.data
		temp = Random_test_id.query.filter(Random_test_id.subject == subject).filter(Random_test_id.topic == topic).all()
		if len(temp)==0 :
			data = Random_test_id(
				student_id = current_user.id,
				subject = subject,
				topic = topic,
			)
			db.session.add(data)
			db.session.commit()
			temp = Random_test_id.query.filter(Random_test_id.subject == subject).filter(Random_test_id.topic == topic).one()
			id = temp.id
			l = [topic]
			questions = Questions.query.filter(Questions.category == subject).all()
			c = 1
			for question in questions:
				if question.tags == l:
					print ("here")
					data = Random_test_question(
						random_test_id = id,
						question_id = question.questionid,
						score = c,
						correct = 0,
						incorrect = 0,
					)
					c += 1
					
					db.session.add(data)
					db.session.commit()
		
		temp = Random_test_id.query.filter(Random_test_id.subject == subject).filter(Random_test_id.topic == topic).one()
		id = temp.id

		temp = Random_test_question.query.with_entities(Random_test_question.question_id).filter(Random_test_question.random_test_id == id).order_by(Random_test_question.score).limit(20).all()
		l = []
		for x in temp:
			l.append(x[0])
		print (l)
		password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) 
		now = datetime.now()
		print (now)
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
		end = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S")+  timedelta( minutes=20)
		print (now, end)
		test_info =  Test_info(
			creatorid = current_user.id,
			subject = subject,
			topic = topic,
			start_time = now,
			end_time = end,
			duration = 1200,
			password = password,
			neg_mark = True,
			show_result = True,
			type = 1
		)
		db.session.add(test_info)
		db.session.commit()

		testdata = Test(
            testid=test_info.testid,
            selected=l,
        )
		db.session.add(testdata)
		db.session.commit()

		return redirect(url_for('practice.start_practice_test',testid = test_info.testid ) )	
	return render_template('practice_test.html',form= form)

@practice.route('/practice-test/start/<testid>', methods=['GET', 'POST'])
@login_required
def start_practice_test(testid):
	form = PracticeTest(request.form)
	if request.method == 'GET':
		test_info = Test_info.query.filter(Test_info.testid == testid).one()
		form = TestForm(test_id=test_info.testid, password=test_info.password)
		return render_template('give_test.html', form = form)

	return render_template('practice_test.html',form= form)




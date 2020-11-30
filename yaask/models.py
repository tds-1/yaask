from yaask import db, login_manager
from passlib.context import CryptContext
import datetime
from flask_login import UserMixin
from datetime import timedelta


SCHEMES = 'pbkdf2_sha256'
pwd_context = CryptContext(
    schemes=[SCHEMES],
    default=SCHEMES,
    pbkdf2_sha256__default_rounds=30000
    )

@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.id == int(userid)).first()


class User(db.Model):
	__tablename__= 'yaask_user'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	username = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	phone_no = db.Column(db.String, nullable=False)
	phone_verified = db.Column(db.Boolean, nullable=True)
	password = db.Column(db.String, nullable=False)
	role = db.Column(db.String, nullable=False)
	score = db.Column(db.Integer, nullable=False)
	answered = db.Column(db.PickleType)
	picture = db.Column(db.String)
	prime = db.Column(db.Boolean, nullable = True)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __init__(self, name, username, email, phone_no, password, score, role, phone_verified, picture):
		self.name = name
		self.username = username
		self.email = email
		self.phone_no = phone_no
		self.password = pwd_context.encrypt(password) 
		self.score = score
		self.phone_verified= phone_verified
		self.role = role
		self.picture = picture

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def __repr__(self):
		return "<Username is '%s'" % (self.username)

class Questions(db.Model):
	__tablename__ = 'questions'

	questionid = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String, nullable=False)
	a = db.Column(db.String, nullable=False)
	b = db.Column(db.String, nullable=False)
	c = db.Column(db.String, nullable=False)
	d = db.Column(db.String, nullable=False)
	answer = db.Column(db.String, nullable=False)
	creatorid = db.Column(db.String, nullable=False)
	category = db.Column(db.String, nullable=False)
	difficulty = db.Column(db.String, nullable=False)
	question_score=db.Column(db.Integer,nullable=False)
	attempts = db.Column(db.Integer,nullable=True)
	comment=db.Column(db.String,nullable=True)
	tags = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, question, a, b, c, d, answer, creatorid, category, difficulty,question_score,comment,tags,attempts):
		self.question = question
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.answer = answer
		self.creatorid = creatorid
		self.category = category
		self.difficulty = difficulty
		self.question_score=question_score
		self.comment=comment
		self.tags=tags
		self.attempts=attempts
			
	def __repr__(self):
		return "<Question id is %s and creatorid is %s" % (self.questionid, self.creatorid)

class Test(db.Model):
	__tablename__ = 'test'

	testid = db.Column(db.Integer, primary_key=True)
	selected = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow() + timedelta(hours=5.5))

	def __init__(self,testid, selected):
		self.testid = testid
		self.selected = selected
	
	def __repr__(self):
		return "<Test id is %s " % (self.testid)


class Test_info(db.Model):
	__tablename__ = 'test_information'

	testid = db.Column(db.Integer, primary_key=True)
	creatorid = db.Column(db.Integer, nullable=False)
	subject = db.Column(db.String, nullable=False)
	topic = db.Column(db.String, nullable=False)
	start_time = db.Column(db.String, nullable=False)
	end_time = db.Column(db.String, nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	password = db.Column(db.String, nullable=False)
	show_result = db.Column(db.Boolean, nullable=False)
	neg_mark = db.Column(db.Boolean, nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	type = db.Column(db.Integer, nullable=False)

	def __init__(self,creatorid , subject, topic, start_time, end_time, duration, password, neg_mark, show_result, type):
		self.creatorid = creatorid
		self.subject = subject
		self.topic = topic
		self.start_time = start_time
		self.end_time = end_time
		self.duration = duration
		self.password = password
		self.neg_mark=neg_mark
		self.show_result=show_result
		self.type = type

	def __repr__(self):
		return "<Test id is %s " % (self.testid)



class Student_test_info(db.Model):
	__tablename__ = 'studenttestinfo'

	id = db.Column(db.Integer, primary_key= True, autoincrement=True)
	username = db.Column(db.String, nullable= False)
	testid = db.Column(db.String, nullable=False)
	time_started = db.Column(db.String, nullable=True)
	completed = db.Column(db.Boolean, default=False)
	time_taken = db.Column(db.PickleType)
	def __init__(self,username, testid, time_started, completed, time_taken):
		self.username = username
		self.testid = testid
		self.time_started = time_started
		self.completed = completed
		self.time_taken = time_taken
		
	def __repr__(self):
		return "<Test id is %s " % (self.testid)



class Students(db.Model):
	__tablename__ = 'students'

	id = db.Column(db.Integer, primary_key= True)
	userid = db.Column(db.Integer, nullable=True)
	testid = db.Column(db.String, nullable=False)
	quid = db.Column(db.String, nullable=False)
	ans = db.Column(db.String, nullable=False)

	def __init__(self,userid, testid, quid, ans):
		self.userid = userid
		self.testid = testid
		self.quid = quid
		self.ans = ans
		
	def __repr__(self):
		return "<Test id is %s " % (self.testid)


class Random_test_id(db.Model):
	__tablename__ = 'random_test_id'

	id = db.Column(db.Integer, primary_key= True)
	student_id = db.Column(db.Integer, nullable=False)
	subject = db.Column(db.String, nullable=False)
	topic = db.Column(db.String, nullable=False)

	def __init__(self, student_id, subject, topic):
		self.student_id = student_id
		self.subject = subject
		self.topic = topic
		
	def __repr__(self):
		return "<Id is %s " % (self.id)

class Random_test_question(db.Model):
	__tablename__ = 'random_test_question'

	id = db.Column(db.Integer, primary_key= True)
	random_test_id = db.Column(db.Integer, nullable=False)
	question_id = db.Column(db.Integer, nullable=False)
	score = db.Column(db.Integer, nullable=False)
	correct = db.Column(db.Integer, nullable=False, default = 0)
	incorrect = db.Column(db.Integer, nullable=False, default = 0)
	left = db.Column(db.Integer, nullable=True, default = 0)
	
	def __init__(self, random_test_id, question_id, score, correct, incorrect, left):
		self.random_test_id = random_test_id
		self.question_id = question_id
		self.score = score
		self.correct = correct
		self.incorrect = incorrect
		self.left = left

	def __repr__(self):
		return "<Id is %s " % (self.id)



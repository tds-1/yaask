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
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, name, username, email, phone_no, password, score, role, phone_verified):
		self.name = name
		self.username = username
		self.email = email
		self.phone_no = phone_no
		self.password = pwd_context.encrypt(password) 
		self.score = score
		self.phone_verified= phone_verified
		self.role = role

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

	question = db.Column(db.String, nullable=False)
	a = db.Column(db.String, nullable=False)
	b = db.Column(db.String, nullable=False)
	c = db.Column(db.String, nullable=False)
	d = db.Column(db.String, nullable=False)
	answer = db.Column(db.String, nullable=False)
	creatorid = db.Column(db.String, nullable=False)
	questionid = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String, nullable=False)
	difficulty = db.Column(db.String, nullable=False)
	question_score=db.Column(db.Integer,nullable=False)
	comment=db.Column(db.String,nullable=True)
	tags = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, question, a, b, c, d, answer, creatorid, category, difficulty,question_score,comment,tags):
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
			
	def __repr__(self):
		return "<Question id is %s and creatorid is %s" % (self.questionid, self.creatorid)

class Test(db.Model):
	__tablename__ = 'test1'

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
	start_date = db.Column(db.Date, nullable=False)
	start_time = db.Column(db.Time, nullable=False)
	end_date = db.Column(db.Date, nullable=False)
	end_time = db.Column(db.Time, nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	password = db.Column(db.String, nullable=False)
	show_result = db.Column(db.Boolean, nullable=False)
	neg_mark = db.Column(db.Boolean, nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __init__(self,creatorid , subject, topic, start_date, start_time, end_date, end_time, duration, password, neg_mark, show_result):
		self.creatorid = creatorid
		self.subject = subject
		self.topic = topic
		self.start_date = start_date
		self.start_time = start_time
		self.end_date = end_date
		self.end_time = end_time
		self.duration = duration
		self.password = password
		self.neg_mark=neg_mark
		self.show_result=show_result
		
	def __repr__(self):
		return "<Test id is %s " % (self.testid)



class Student_test_info(db.Model):
	__tablename__ = 'studenttestinfo'

	id = db.Column(db.Integer, primary_key= True, autoincrement=True)
	username = db.Column(db.String, nullable= False)
	testid = db.Column(db.String, nullable=False)
	time_left = db.Column(db.Integer, nullable=False)
	completed = db.Column(db.Boolean, default=False)

	def __init__(self,username, testid, time_left, completed):
		self.username = username
		self.testid = testid
		self.time_left = time_left
		self.completed = completed
		
	def __repr__(self):
		return "<Test id is %s " % (self.testid)



class Students(db.Model):
	__tablename__ = 'students'

	id = db.Column(db.Integer, primary_key= True)
	username = db.Column(db.String, nullable=True)
	testid = db.Column(db.String, nullable=False)
	quid = db.Column(db.String, nullable=False)
	ans = db.Column(db.String, nullable=False)

	def __init__(self,username, testid, quid, ans):
		self.username = username
		self.testid = testid
		self.quid = quid
		self.ans = ans
		
	def __repr__(self):
		return "<Test id is %s " % (self.testid)



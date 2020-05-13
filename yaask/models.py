from yaask import db, login_manager
from passlib.context import CryptContext
import datetime
from flask_login import UserMixin

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
	__tablename__= 'quizuser1'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	username = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	phone_no = db.Column(db.String, nullable=False)
	phone_verified = db.Column(db.Boolean, nullable=False)
	password = db.Column(db.String, nullable=False)
	score = db.Column(db.Integer, nullable=False)
	answered = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, name, username, email, phone_no, password, score):
		self.name = name
		self.username = username
		self.email = email
		self.phone_no = phone_no
		self.password = pwd_context.encrypt(password) 
		self.score = score

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
	__tablename__ = 'quizquestions1'

	question = db.Column(db.String, nullable=False)
	option1 = db.Column(db.String, nullable=False)
	option2 = db.Column(db.String, nullable=False)
	option3 = db.Column(db.String, nullable=False)
	option4 = db.Column(db.String, nullable=False)
	answer = db.Column(db.String, nullable=False)
	creatorid = db.Column(db.String, nullable=False)
	questionid = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String, nullable=False)
	difficulty = db.Column(db.String, nullable=False)
	question_score=db.Column(db.Integer,nullable=False)
	comment=db.Column(db.String,nullable=True)
	tags = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, question, option1, option2, option3, option4, answer, creatorid, category, difficulty,question_score,comment,tags):
		self.question = question
		self.option1 = option1
		self.option2 = option2
		self.option3 = option3
		self.option4 = option4
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
	creatorid = db.Column(db.Integer, nullable=False)
	selected = db.Column(db.PickleType)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __init__(self, creatorid, selected):
		self.creatorid = creatorid
		self.selected = selected
	
	def __repr__(self):
		return "<Test id is %s and creatorid is %s" % (self.testid, self.creatorid)



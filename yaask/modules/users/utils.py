from itsdangerous import URLSafeTimedSerializer
from os import environ
from yaask import mail
from flask_mail import Message

try:
    from yaask.config import SECRET_KEY, SECURITY_PASSWORD_SALT
    SECRET_KEY = SECRET_KEY
    SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT 
except:
    SECRET_KEY = environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = environ['SECURITY_PASSWORD_SALT']


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    MAIL_ID = MAIL_ID = "yaasklabsauth@gmail.com"
    msg = Message(subject,
        sender=("Admin", MAIL_ID), 
	    recipients=[to],
        html=template
    )
    mail.send(msg)


from passlib.apps import custom_app_context as pwd_context
from mongokit import ValidationError, Document
import datetime
import re


def email_validator(value):
    email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)
    if not bool(email.match(value)):
        raise ValidationError('%s is not a valid email')
    else:
        return True


class User(Document):
    __database__ = 'sample_app'
    __collection__ = 'users'
    use_dot_notation = True
    raise_validation_errors = False
    structure = {
        "id": int,
        "username": unicode,
        "password_hash": unicode,
        "created": datetime.datetime,
        "updated": datetime.datetime,
        "last_login": datetime.datetime
    }
    validators = {
        'username': email_validator
    }
    required_fields = ['username', 'password_hash']
    default_values = {
        'created': datetime.datetime.utcnow,
        'updated': datetime.datetime.utcnow,
        'last_login': datetime.datetime.utcnow
    }

    def __repr__(self):
        return '<User %r>' % (self.username)

    def hash_password(self, password):
        return unicode(pwd_context.encrypt(password))

    def verify_password(self, password):
        print self.password_hash
        return pwd_context.verify(password, self.password_hash)

    def get_next_user_id(self):
        return self.query.filter({"username": "next_user_id", "password_hash": "thisisapassword"}).first()






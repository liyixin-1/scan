from sqlalchemy.exc import SQLAlchemyError

from app import db
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from marshmallow import post_load

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phonenumber=db.Column(db.String(11))
    email=db.Column(db.String(20))
    role = db.Column(db.String(20))

    def __init__(self, username, password,phonenumber,email, role):
      self.username = username
      self.password = password
      self.phonenumber=phonenumber
      self.email=email
      self.role = role

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
      return session_commit()

    def updatepasswd(self,username,password):
      self.query.filter_by(username=username).update({'password':password})
      db.session.commit()
      return self

    def delete(self, username):
      self.query.filter_by(username=username).delete()
      return session_commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


def session_commit():
  try:
    db.session.commit()
  except SQLAlchemyError as e:
    db.session.rollback()
    reason = str(e)
    return reason

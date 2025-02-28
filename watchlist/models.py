from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from watchlist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    code = db.Column(db.String(10))
    uptimes=db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)

class Stockvo():
    def __init__(self,id,name ,code,uptimes,percent,lbc,zj,hs):
        self.id = id
        self.name = name
        self.code = code
        self.uptimes = uptimes
        #self.timestamp = timestamp
        self.percent = percent
        self.lbc = lbc
        self.zj = zj
        self.hs = hs

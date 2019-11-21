from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship('Reservation', backref='Reservator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ClassroomNum = db.Column(db.Integer, unique=True)
    reservations = db.relationship('Reservation', backref="Reserved_Classroom", lazy='dynamic')

    def __repr__(self):
        return '<Classroom {}>'.format(self.ClassroomNum)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromTime = db.Column(db.DateTime)
    toTime = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    classroom_num = db.Column(db.Integer)

    def __repr__(self):
        return '<Classroom {}>'.format(self.fromTime.time())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


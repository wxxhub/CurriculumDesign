#coding: utf-8

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField

from app.db_manager import db, login_manager

# from app.

__all__ = ['Manager', 'Question', 'Charactor', 'User']

manager_app = Blueprint('manager', __name__, url_prefix="/manager")
user_app = Blueprint('user', __name__, url_prefix="/user") 

class Manager(db.Model):
    __tablename__ = 'manager'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, manager_name='master', manger_password='111111'):
        self.name = manager_name
        self.password = manger_password
    
    def __repr__(self):
        return '<User %r>' % self.name

    def todict(self):
        return self.__dict__

#下面这4个方法是flask_login需要的4个验证方式
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # def password(self, password):
    #     self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class User(db.Model):
    __tablename__ = 'user'

    # id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8))
    character = db.Column(db.String(32))

    def __init__(self,number = 160111111, name='user0', character='111111'):
        self.number = number
        self.name = name
        self.character = character

class UserForm(Form):
    number = StringField('编号')
    name = StringField('姓名')
    character = StringField('性格')
    submit = SubmitField('添加')

@login_manager.user_loader
def load_manager(manager_id, endpoint='user'):
    print ('test:'+endpoint)
    return Manager.query.get(int(manager_id))


class Question(db.Model):
    __tablename__ = 'question'

    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    result1 = db.Column(db.String(16))
    result2 = db.Column(db.String(16))
    result3 = db.Column(db.String(16))

class QuestionForm(Form):
    number = StringField('题目编号')
    name = StringField('题目')
    result1 = StringField('答案1')
    result2 = StringField('答案2')
    result3 = StringField('答案3')
    submit = SubmitField('添加')


class Character(db.Model):
    __tablename__ = 'Character'
    score = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(32))
    character_details = db.Column(db.String(255))

class CharacterForm(Form):
    score = StringField('分数')
    character = StringField('性格')
    character_details = StringField('性格详情')
    submit = SubmitField('添加')
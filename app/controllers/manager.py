#coding: utf-8
import re
from datetime import datetime

from flask import Blueprint, render_template
from flask import redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app.models import *
from app.db_manager import db, login_manager

manager_bp = Blueprint(
    'manager',
    __name__,
    template_folder='../templates'
)

@manager_bp.route("/manager_login")
def managerLogin():
    return render_template('managerLogin.html')
    # return 'test'

@manager_bp.route("/manager_commit")
def managerCommit():
    login_name = request.args['username']
    psw = request.args['psw']

    # managers = Manager.query.all()
    # for t in managers:
    #     db.session.delete(t)
    #     db.session.commit()

    origin_master = Manager.query.filter_by(name='master').first()
    if not origin_master:
        origin_master = Manager()
        db.session.add(origin_master)
        db.session.commit()
    
    managers = Manager.query.all()
    for t in managers:
        print (t.password)

    m = Manager.query.filter_by(name=login_name).first()
    if m and m.password == psw:
        login_user(m)
        db.session.commit()
        print (m)
        return redirect(url_for('manager.toWelcomeManager'))
    else:
        return '账号或密码错误'

@manager_bp.route("/to_welcome_manager")
@login_required
def toWelcomeManager():
    return render_template('welcome_manager.html')

@manager_bp.route("/welcome_manager")
@login_required
def welcomeManager():
    value = request.values.get("button")

    print (value)
    if value == "管理测试结果": 
        return redirect(url_for('manager.addRoot'))
    elif value == "管理测试题目": 
        return redirect(url_for('manager.addQuestion'))
    elif value == "管理用户": 
        return redirect(url_for('manager.managerUser'))  

@manager_bp.route("/add_data")
@login_required
def addRoot():
    characters = Character.query.all()
    form = CharacterForm()
    return render_template('add_data.html', form=form, characters=characters)

@manager_bp.route("/add", methods=['POST'])
@login_required
def addData():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character()
        form.populate_obj(character)
        db.session.add(character)
        db.session.commit()
    return redirect(url_for('manager.addRoot'))


@manager_bp.route('/delete', methods=['POST'])
@login_required
def deleteData():
    value = request.values.get("button")
    s_option =  request.values.getlist("test")

    if value == "删除所选项目":
        character = Character
        for s in s_option:
            character = Character.query.filter_by(score=s).first()
            db.session.delete(character)
            db.session.commit()
    return redirect(url_for('manager.addRoot'))

@manager_bp.route("/add_question_data")
@login_required
def addQuestion():
    questions = Question.query.all()
    form = QuestionForm()
    return render_template('add_question.html', form=form, questions=questions)

@manager_bp.route("/add_question", methods=['POST'])
@login_required
def addQuestionData():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question()
        form.populate_obj(question)
        db.session.add(question)
        db.session.commit()
    return redirect(url_for('manager.addQuestion'))


@manager_bp.route('/delete_question', methods=['POST'])
@login_required
def deleteQuestionData():
    value = request.values.get("button")
    s_option =  request.values.getlist("test")

    if value == "删除所选项目":
        for s in s_option:
            question = Question.query.filter_by(number=s).first()
            db.session.delete(question)
            db.session.commit()
    return redirect(url_for('manager.addQuestion'))

@manager_bp.route("/manager_user")
@login_required
def managerUser():
    users = User.query.all()
    characters = Character.query.all()
    user_size = User.query.count()

    character_sizes = []

    for c in characters:
        character_sizes.append(0)

    form = UserForm()
    return render_template('manager_user.html', form=form, users=users, characters=characters, user_size=user_size, character_sizes=character_sizes)

@manager_bp.route("/add_user", methods=['POST'])
@login_required
def addUser():
    form = UserForm()
    if form.validate_on_submit():
        question = User()
        form.populate_obj(question)
        db.session.add(question)
        db.session.commit()
    return redirect(url_for('manager.managerUser'))

@manager_bp.route('/delete_user', methods=['POST'])
@login_required
def deleteUserData():
    value = request.values.get("button")
    s_option =  request.values.getlist("test")
    if value == "删除所选项目":
        for s in s_option:
            user = User.query.filter_by(number=s).first()
            db.session.delete(user)
            db.session.commit()
    return redirect(url_for('manager.managerUser'))
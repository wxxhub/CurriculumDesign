#coding: utf-8
import re
from datetime import datetime

from flask import Blueprint, render_template
from flask import redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app.models import *
from app.db_manager import db, login_manager

from .config import getConfigResult, setConfig

manager_bp = Blueprint(
    'manager',
    __name__,
    template_folder='../templates'
)

open_identifi = '打开编号姓名认证'
close_identifi = '关闭编号姓名认证'
user_forms = []

class UserData():
    number = 0
    name = ''

    # def __init__(self, o_number, o_name):
    #     number = o_number
    #     name = o_name

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
    # for t in managers:
    #     print (t.password)

    m = Manager.query.filter_by(name=login_name).first()
    if m and m.password == psw:
        login_user(m)
        db.session.commit()
        # print (m)
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

    # print (value)
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
    # test_user_size = User().query.filter(User.character!=None).count()
    test_user_size = 0
    

    character_sizes = []
    character_ratios = []

    config_result = getConfigResult()
    config = ''
    config_submit = ''

    if config_result == 0:
        config = '编号姓名认证已关闭'
        config_submit = open_identifi
    else:
        config = '编号姓名认证已开启'
        config_submit = close_identifi

    for u in users:
        # print (u.character)
        if u.character:
            test_user_size += 1

    for c in characters:
        size = User.query.filter_by(character=c.character).count()
        character_sizes.append(size)
        if test_user_size == 0:
            character_ratios.append(0)
        else:
            character_ratios.append(1.0 * size / test_user_size)

    form = UserForm()
    return render_template('manager_user.html',
                            form=form,
                            users=users,
                            characters=characters,
                            user_size=user_size,
                            test_user_size=test_user_size,
                            character_sizes=character_sizes, 
                            character_ratios=character_ratios,
                            config=config,
                            config_submit=config_submit)

@manager_bp.route("/add_user", methods=['POST'])
@login_required
def addUser():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.character = None
        form.populate_obj(user)
        db.session.add(user)
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

@manager_bp.route('/to_import')
@login_required
def toImport():
        return render_template('import_user.html')

@manager_bp.route('/import_user')
@login_required
def importUser():
    value = request.values.get("file")
    button = request.values.get("button")
    global user_forms
    user_forms.clear()
    # print (value)
    if value:
        import xlwt
        import xlrd
        xlsfile = value
        book = xlrd.open_workbook(xlsfile)
        sheet0 = book.sheet_by_index(0)
        nrows = sheet0.nrows    # 获取行总数
        
        # print (button)
        if button == "导入用户":
            number_x = int(request.values.get("number_x")) - 1
            name_x = int(request.values.get("name_x")) - 1
            start_y = int(request.values.get("start_y")) - 1
            for i in range(start_y, nrows):
                form = UserData()
                form.number = int(sheet0.cell_value(i,number_x))
                form.name = str(sheet0.cell_value(i,name_x))
                user_forms.append(form)
                print (str(int(sheet0.cell_value(i,number_x)))+"  "+str(sheet0.cell_value(i,name_x)))

            return render_template('ensure_import.html',forms=user_forms)

    return render_template('import_user.html')

@manager_bp.route('/ensure_user')
@login_required
def ensureUser():
    button = request.values.get("button")
    if button == "确认导入":
        # print (user_forms.number)
        for form in user_forms:
            u = User.query.filter_by(number=form.number).first()
            if not u:
                user = User(form.number, form.name, "")
                db.session.add(user)
                db.session.commit()
            # print (form.name)
    user_forms.clear()
    return redirect(url_for('manager.managerUser'))

@manager_bp.route('/config')
@login_required
def configData():
    getConfigResult()
    value = request.values.get("button")
    if value == open_identifi:
        setConfig(1)
    else:
        setConfig(0)
    return redirect(url_for('manager.managerUser'))

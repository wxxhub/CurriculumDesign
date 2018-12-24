from flask import Flask, request, flash
from flask_sqlalchemy import SQLAlchemy
# from flask_security import RoleMixin, UserMixin

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField

from flask import Blueprint, render_template
from flask import url_for, redirect

# import flask_login
from flask_login import LoginManager, current_user, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///character_test.db'
app.config['SECRET_KEY'] = 'please, tell nobody'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "managerLogin"  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 定义需要登录访问页面的提示消息

# manager_login = False

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


@login_manager.user_loader
def load_manager(manager_id, endpoint='user'):
    print ('test:'+endpoint)
    return Manager.query.get(int(manager_id))

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
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # class Question

class Question(db.Model):
    __tablename__ = 'question'

    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    result1 = db.Column(db.String(16))
    result2 = db.Column(db.String(16))
    result3 = db.Column(db.String(16))
    # result4 = db.Column(db.String(16))

class QuestionForm(Form):
    number = StringField('题目编号')
    name = StringField('题目')
    result1 = StringField('答案1')
    result2 = StringField('答案2')
    result3 = StringField('答案3')
    submit = SubmitField('添加')

class User(db.Model):
    __tablename__ = 'user'

    # id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    character = db.Column(db.String(32))
    password = db.Column(db.String(32))

class UserForm(Form):
    number = StringField('编号')
    name = StringField('姓名')
    character = StringField('性格')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/direct")
def direct():
    value = request.values.get("direct")

    print (value)
    if value == "开始问卷调查": 
        return redirect(url_for('startExamen'))
    elif value == "管理数据库": 
        return redirect(url_for('managerLogin'))

@app.route("/examen")
def startExamen():
    questions = Question.query.all()
    form = QuestionForm()
    size = 0
    for q in questions:
        size += 1
    return render_template('examen.html', form=form, questions=questions, question_size = size)

@app.route("/submit_result")
def submitResult():
    questions = Question.query.all()
    size = 0
    for q in questions:
        size += 1

    score = 0
    i = 1
    while i <= size:
        value = request.values.get("question%d"%i)
        if value:
            if value == 'A':
                score += 8
            elif value == 'B':
                score += 4
            elif value == 'C':
                score += 1
            else:
                print ('没有选项')
        # else:
        #     return (alert("你好，我是一个警告框！"))
        i += 1
        print (value)
    
    result_character = Character().query.filter_by(score=0).first()
    characters = Character.query.all()
    for c in characters:
        if c.score < score:
            result_character = c
        else:
            break
    if result_character:
        return render_template('show_result.html', character=result_character)
    else:
        return ('faile')

@app.route("/manager_login")
def managerLogin():
    return render_template('managerLogin.html')

@app.route("/manager_commit")
def managerCommit():
    login_name = request.args['username']
    psw = request.args['psw']

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
        # manager = Manager()
        login_user(m)
        m.last_login = datetime.now()
        # db.session.commit()
        print (m)
        return redirect(url_for('toWelcomeManager'))
    else:
        return '账号或密码错误'

@app.route("/to_welcome_manager")
@login_required
def toWelcomeManager():
    return render_template('welcome_manager.html')

@app.route("/welcome_manager")
@login_required
def welcomeManager():
    value = request.values.get("button")

    print (value)
    if value == "管理测试结果": 
        return redirect(url_for('addRoot'))
    elif value == "管理测试题目": 
        return redirect(url_for('addQuestion'))
    elif value == "管理用户": 
        return redirect(url_for('managerUser')) 

@app.route("/add_data")
@login_required
def addRoot():
    characters = Character.query.all()
    form = CharacterForm()
    return render_template('add_data.html', form=form, characters=characters)

@app.route("/add", methods=['POST'])
@login_required
def addData():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character()
        form.populate_obj(character)
        db.session.add(character)
        db.session.commit()
    return redirect(url_for('addRoot'))


@app.route('/delete', methods=['POST'])
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
    return redirect(url_for('addRoot'))

@app.route("/add_question_data")
@login_required
def addQuestion():
    questions = Question.query.all()
    form = QuestionForm()
    return render_template('add_question.html', form=form, questions=questions)

@app.route("/add_question", methods=['POST'])
@login_required
def addQuestionData():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question()
        form.populate_obj(question)
        db.session.add(question)
        db.session.commit()
    return redirect(url_for('addQuestion'))


@app.route('/delete_question', methods=['POST'])
@login_required
def deleteQuestionData():
    value = request.values.get("button")
    s_option =  request.values.getlist("test")

    if value == "删除所选项目":
        for s in s_option:
            question = Question.query.filter_by(number=s).first()
            db.session.delete(question)
            db.session.commit()
    return redirect(url_for('addQuestion'))

@app.route("/manager_user")
@login_required
def managerUser():
    # s_option = User.query.all()

    # db.session.delete(User)
    # db.session.commit()

    users = User.query.all()
    form = UserForm()
    return render_template('manager_user.html', form=form, users=users)


# UserData.query.filter_by(username='name').delete()

if __name__ == '__main__':
    db.create_all()
    # app.run(host = '192.168.43.121' ,port = 5000, debug = 'True')
    app.run()
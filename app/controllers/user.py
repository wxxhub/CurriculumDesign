from flask import Blueprint, render_template
from flask import redirect, request, url_for
from flask_login import login_user, logout_user, current_user

from app.models import User, Question, QuestionForm, Character, CharacterForm

user_bp = Blueprint(
    'user',
    __name__,
    template_folder='../templates'
)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route("/direct")
def direct():
    value = request.values.get("direct")

    print (value)
    if value == "开始问卷调查": 
        return redirect(url_for('user.startExamen'))
    elif value == "管理数据库": 
        return redirect(url_for('manager.managerLogin'))

@user_bp.route("/examen")
def startExamen():
    questions = Question.query.all()
    form = QuestionForm()
    size = 0
    for q in questions:
        size += 1
    return render_template('examen.html', form=form, questions=questions, question_size = size)

@user_bp.route("/submit_result")
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
        return 'test'
    else:
        return ('faile')
#coding: utf-8

from flask import Flask, render_template
from .controllers import blueprints
from .db_manager import db, login_manager

def createApp(config_name = None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///character_test.db'
    app.config['SECRET_KEY'] = 'please, tell nobody'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    for bp in blueprints:
        app.register_blueprint(bp)

    # error handler
    handle_errors(app)

    db.init_app(app)
    login_manager.init_app(app)

    return app

def handle_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    @app.errorhandler(403)
    def acess_forbidden_error(error):
        return '403'

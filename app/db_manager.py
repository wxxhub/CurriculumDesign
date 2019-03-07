# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# db
db = SQLAlchemy()

# login_manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "manager.managerLogin"  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 定义需要登录访问页面的提示消息

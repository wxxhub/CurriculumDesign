#coding: utf-8

from .manager import manager_bp
from .user import user_bp

blueprints = [
    manager_bp,
    user_bp
]
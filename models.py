# encoding:utf8
# 存放模型

# exts.py
# models_sep.py

from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11))
    password = db.Column(db.String(100), nullable=False)
    authority = db.Column(db.Integer, default=0)


class Alarm(db.Model):
    __tablename__ = 'alarm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 预警id
    type = db.Column(db.Integer, default=1)  # 预警类型， 1：ST预警
    create_time = db.Column(db.DateTime, default=datetime.now)  # 预警时间
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 提交用户
    filename = db.Column(db.String(50))  # 文件名
    # result = db.Column(db.String(200))  # 结果

    result_1 = db.Column(db.Float)
    result_2 = db.Column(db.Float)
    result_3 = db.Column(db.Float)
    result_4 = db.Column(db.Float)

    author = db.relationship('User', backref=db.backref('alarms'))

# encoding:utf-8
# 存放配置文件

import os

DEBUG = False

# SECRET_KEY = os.urandom(24)
SECRET_KEY = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'edith'

DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                      DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

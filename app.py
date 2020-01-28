# encoding:utf-8

# 从flask框架中导入Flask类

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from functools import wraps
from flask import make_response, jsonify
import os
import config
import pandas as pd

# ST 鉴定
from mymodels.get_model_result_1 import get_result

# ST 预警
from mymodels.get_model_result_2 import get_alarm_result

from exts import db
from models import User, Alarm

# 初始化一个Flask对象，需要传递一个参数__name__
# 1.方便Flask框架去寻找资源
# 2.方便Flask插件比如Flask-Sqlalchemy出现错误时好去寻找位置
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 登陆限制的装饰器
# 可以独立建立一个decorators.py
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


# app.route是一个装饰器（开头，在函数上去），做一个url与视图函数的映射
# http://127.0.0.1:5000/   去请求hello_world函数，然后将结果返回给浏览器
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template("index.html")


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/st_alarm_intro', methods=['GET', 'POST'])
def st_alarm_intro():
    return render_template("st_alarm_intro.html")


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get("username")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        context = {
            'username': username,
            'phone': phone,
            'password': password,
            'confirmpassward': confirmpassword,
            'register_error': "",
        }

        # 密码验证
        if (password != confirmpassword):
            context['register_error'] = "两次密码输入不一致"
            return render_template("register.html", **context)
        elif (len(password) < 4):
            context['register_error'] = "密码不得少于四位"
            return render_template("register.html", **context)
        else:
            user = User.query.filter(User.username == username).first()
            if user:
                context['register_error'] = "该账号已被注册"
                return render_template("register.html", **context)
            else:
                user = User(username=username, phone=phone, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username == username, User.password == password).first()

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_authority'] = user.authority
            session.permanent = True
            return redirect(url_for('index'))
        else:
            context = {
                'username': username,
                'password': password,
            }
            return render_template("login.html", **context, login_error="用户名或密码错误")


# 登出
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


# 用户：用户信息查看
@app.route('/user_detail/<user_id>')
@login_required
def user_detail(user_id):
    user_model = User.query.filter(User.id == user_id).first()
    # user.details
    return render_template('user_detail.html', user=user_model)


# 用户：修改密码
@app.route('/user_update_password/<user_id>', methods=['GET', 'POST'])
@login_required
def user_update_password(user_id):
    if request.method == 'POST':
        user = User.query.filter(User.id == user_id).first()
        if (user.password != request.form.get("password")):
            return render_template("user_update_password.html", update_error="原密码输入错误")
        elif (request.form.get("newpassword1") != request.form.get("newpassword2")):
            return render_template("user_update_password.html", update_error="两次输入新密码不同")
        else:
            user.password = request.form.get("newpassword1")
            db.session.commit()
            return redirect(url_for('user_detail', user_id=user_id))
    else:
        return render_template("user_update_password.html")


# 管理员：用户信息管理
@app.route('/user_management')
@login_required
def user_management():
    context = {
        'users': User.query.all()
    }
    # every_user.details
    return render_template('user_management.html', **context)


# 管理员：用户信息修改
@app.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    user_id = request.form.get("update_id")
    user = User.query.filter(User.id == user_id).first()
    user.phone = request.form.get("update_phone")
    user.password = request.form.get("update_password")
    db.session.commit()
    return redirect(url_for('user_management'))


# 管理员：用户信息删除
@app.route('/delete_user/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_management'))
    # return jsonify({'result': 200})


# 用户：个人预警记录查看
@app.route('/user_check_alarm/<user_id>')
@login_required
def user_check_alarm(user_id):
    context = {
        'alarms': Alarm.query.filter(Alarm.author_id == user_id).order_by('-create_time').all()
    }
    # user_alarm.details
    return render_template('alarm_user_check.html', **context)


# 管理员：管理预警记录
@app.route('/alarm_management')
@login_required
def alarm_management():
    context = {
        'alarms': Alarm.query.order_by('-create_time').all()
    }
    # every_alarm.details
    return render_template('alarm_management.html', **context)


# st财务鉴别
@app.route('/st_distinguish')
def st_distinguish():
    return render_template("st_distinguish.html")


@app.route('/st_distinguish_upload', methods=['GET', 'POST'])
def st_distinguish_upload():
    if request.method == 'POST':
        myFile = request.files['uploadFile']

        # 判断语句
        if (myFile.content_type == "application/vnd.ms-excel"):
            # 写入文件
            path = os.path.join(os.getcwd(), "userdata", myFile.filename)
            myFile.save(path)
            target_path = os.path.join('userdata', myFile.filename)
            data = pd.read_csv(target_path, encoding='GB18030')
            # data = pd.read_csv('userdata/test_data_1.csv', encoding='GB18030')
            test_x = data.iloc[:, -9:]  # x: x1-x9 特征数据
            datas = get_result(test_x)
            context = {
                'data1': datas[0][0] * 100,
                'data2': datas[1][0] * 100,
                'data3': datas[2][0] * 100
            }

            return render_template('st_alarm.html', **context)
        else:
            print("请输入excel或者csv")
            return render_template("st_alarm.html")


# st 财务预警
@app.route('/st_alarm')
def st_alarm():
    return render_template("st_alarm.html")


@app.route('/st_alarm_upload', methods=['GET', 'POST'])
def st_alarm_upload():
    if request.method == 'POST':
        myFile = request.files['uploadFile']

        # 判断语句
        if (myFile.content_type == "application/vnd.ms-excel"):
            # 判断是否用户是否登录
            if (session.get('user_id')):
                author_id = session['user_id']
                author_name = session['username']
            else:
                author_id = None
                author_name = ''

            # 写入文件
            path = os.path.join(os.getcwd(), 'static', 'user_data', str(author_id) + '_' + myFile.filename)
            myFile.save(path)
            target_path = os.path.join('static', 'user_data', str(author_id) + '_' + myFile.filename)

            try:
                data = pd.read_csv(target_path, encoding='GB18030')
                # data = pd.read_csv('userdata/test_data_1.csv', encoding='GB18030')
                test_x = data.iloc[:, -9:]  # x: x1-x9 特征数据

                datas = get_alarm_result(test_x)
                result_1 = round(datas[0], 2)
                result_2 = round(datas[1], 2)
                result_3 = round(datas[2], 2)
                result_4 = round(datas[3], 2)

                alarm = Alarm(type=1, author_id=author_id, filename=myFile.filename, result_1=result_1,
                              result_2=result_2,
                              result_3=result_3, result_4=result_4)
                db.session.add(alarm)
                db.session.commit()

                context = {
                    'data0': result_1,
                    'data1': result_2,
                    'data2': result_3,
                    'data3': result_4
                }

                return render_template('st_alarm.html', **context)

            except:
                return render_template("st_alarm.html", st_alarm_error="上传csv格式有误，请参考示范模板")

        else:
            return render_template("st_alarm.html", st_alarm_error="请上传csv文件")
    else:
        return redirect(url_for('st_alarm'))


# 如果当前文件作为入口程序运行，执行app.run()
if __name__ == '__main__':
    # 启动一个应用服务器，来接受用户的请求
    app.run()

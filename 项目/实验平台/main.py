#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#flask_bootstrap:
#http://www.jb51.net/article/110841.htm

# pip3 install flask_bootstrap
# pip3 install flask_uploads
# pip3 install gevent

from datetime import timedelta

# from wsgiref.simple_server import make_server 过时了

#Flask实现异步非阻塞请求功能实例解析
#http://www.jb51.net/article/134832.htm
# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

import cx_Oracle
from flask import Flask, request, jsonify, session
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import my_rsa
from autoexec import check_student_url
from my_db import db_user, db_password, db_address

# 猴子补丁仔细的用并行代码副本替换标准socket模块的函数和类，这种方式可以使模块在不知情的情况下让gevent更好的运行于multi-greenlet环境中。
monkey.patch_all()


app = Flask(__name__)

from my_user import User

#对bootstrap进行初始化
#所有没有下面这个配置,访问后面的网站会非常慢:http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap=Bootstrap(app)

# SECRET_KEY是为SESSION对象服务的:
# 它允许你在不同请求间存储特定用户的信息。
# 它是在 Cookies 的基础上实现的，并且对 Cookies 进行密钥签名。
# 这意味着用户可以查看你 Cookie 的内容，但却不能修改它，除非用户知道签名的密钥
# 配置secret_key,否则不能实现session对话
SECRET_KEY = '\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'
AUTH_SALT = 'kafkjsa!@#DSDiewfdsakjoirewq'  #给SECRET_KEY加点盐'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['AUTH_SALT'] = AUTH_SALT


'''
#使用Flask设计带认证token的RESTful API接口[翻译]
# https://www.cnblogs.com/vovlie/p/4182814.html
@auth.get_password与@auth.verify_password二选一,都是一样的
# get_password是关键词,是@auth的内部属性
@auth.get_password
def get_password(username):
    if username == 'myuser':
        return 'mypassword'
    return None
'''
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.permanent=True
login_manager.init_app(app)

# my_user_loader()函数通过”@login_manager.user_loader”装饰器修饰的方法，
# 是我们要实现的加载用户对象方法。
# 它是一个回调函数，在每次请求过来后，Flask-Login都会从Session中读取user的"id"的值，
# 所以,my_user_loader(user_id)中的参数值user_id是系统自动调用session['user_id']获取的
# 如果找到的话，就会用这个”user_id”值来调用此回调函数，
# 并构建一个用户类对象。因此，没有这个回调的话，Flask-Login将无法工作。
# 本例中,user_id为用户名.
# 每次刷新页面的时候,user_loader()函数会被自动调用,并且更新current_user变量.
# 调用current_user变量即可获取当前登录用户的User_id值,
@login_manager.user_loader
def my_user_loader(user_id):
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    sql = "SELECT id,password,name,class,github_username,role,result_sum,web_sum FROM is_analysis_studyinfo where id=:id"
    res = cur.execute(sql, {"id": user_id})
    user=User()
    for row in res:
        user.id = row[0]
        user.password= row[1]
        user.name=row[2]
        user.class_=row[3]
        user.github_username=row[4]
        user.role=row[5]
        user.result_sum = row[6]
        user.web_sum=row[7]
        conn.close()
        #print('每次刷新页面都会调用user_loader() %s,%s,%s,%s,%s' % (user.id,user.name,user.class_,user.role,user.github_username))
        return user
    conn.close()
    #print('每次刷新页面都会调用user_loader() 未登录:%s',user_id)
    return None


def my_split(str,str_split=','):
    if str is None:
        return None
    return str.split(str_split)

#主页
# @app.route("/get_github_user",methods=['GET'])
@app.route("/",methods=['GET'])
def get_github_user():
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    sql = "SELECT id,name,class,github_username,update_date,result_sum,web_sum FROM is_analysis_studyinfo where role='学生' and disable!='是' order by class,id"
    cur.execute(sql)
    students = cur.fetchall()
    sql = "SELECT count(*) FROM is_analysis_testinfo"
    cur.execute(sql)
    test_count_=cur.fetchall()
    test_count=test_count_[0][0]
    conn.close()
    public_key_str = my_rsa.public_key_str
    #如果没有登录,current_user.get_id()返回none
    return render_template('list.html',public_key_str=public_key_str,
                           students=students, user=current_user, test_count=test_count)


# 普通函数,返回学号对应的学生姓名和github账号
def get_one_user(stu_id):
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    sql = "SELECT name,github_username FROM is_analysis_studyinfo where id=:id"
    res = cur.execute(sql,{"id":stu_id})
    name=""
    github_username=""
    for row in res:
        name=row[0]
        github_username=row[1]
    conn.close()
    return name, github_username

#测试命令:
## curl -H "Content-Type: application/json" -X POST --data '{"username":'2',"password":"asdf"}' http://127.0.0.1:8383/login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        #http://www.pythondoc.com/flask-login/
        #http://flask.pocoo.org/docs/0.12/   flask 0.12.2
        #如果浏览器的请求是: headers: 'Content-Type': 'multipart/form-data'
        #username = request.form['username']
        #password = request.form['password']

        #如果浏览器的请求是:headers: 'Content-Type': 'application/json'
        #username = request.json['username']
        #str_base64_password = request.json['password']

        user_id = request.form.get('user_id')
        str_base64_password = request.form.get('encrypt_password')
        user_role = request.form.get('user_role')
        print('收到的登录信息:%s,%s,%s' % (user_id,user_role,str_base64_password))

        password = my_rsa.decrypt(str_base64_password) #用私钥解密
        print('用私钥解密出的密码是:%s' % password)

        generate_password = generate_password_hash(password)
        print('应存储到数据库的值是:%s' % generate_password)

        '''
        conn = cx_Oracle.connect(db_user, db_password, db_address)
        cur = conn.cursor()
        sql = "SELECT id,password FROM is_analysis_studyinfo where id=:id and role=:role"
        res = cur.execute(sql, {"id": user_id,"role":user_role})
        db_id = ""
        db_password = ""
        for row in res:
            db_id = row[0]
            db_password = row[1]
        conn.close()
        '''

        user = my_user_loader(user_id)
        if user is None or user.role != user_role:
            return "学号不存在或者类型不匹配."

        if (user.password is None and not user.id == password ) or (user.password is not None and not check_password_hash(user.password, password)):
            return '密码不正确'


        # 设置Session到期时间
        # Session的到期时间为1分钟,或者直接写成整数60,表示60秒.注意,这里是"app.***"
        # 见:#http://www.pythondoc.com/flask/config.html
        # 这句话是配置,可以放到最前面.但下一句session.permanent只能在这里,因为这是session才有意义
        app.permanent_session_lifetime = timedelta(minutes=60)
        session.permanent = True  # 注意,这里是"session.***",而上一语是"app.***"  必须有:app.config['SECRET_KEY'] = SECRET_KEY

        # login_user()这个调用最重要,它将user.id加密写入客户端的Cookie['session']中,内容中只有'user_id'
        # user_id加密保存,加密的Key是:app.secret_key
        # cookie['session']的属性"脚本可访问"为否,即前端js代码不能直接调用getCookie('session')访问该属性.
        # session的读取和解密由Flask的@login_manager.user_loader指定的函数自动完成

        login_user(user, remember=False)

        '''
        # 如果请求中有next参数，则重定向到其指定的地址，
        # 没有next参数，则重定向到"index"视图
        csrf_token = user.generate_auth_token()
        # flask.response.set_cookie('csrf_token', csrf_token)
        print('登录成功:%s,csrf_token=%s' % (username, csrf_token))
        flask.session['id2']=user.id
        '''
        return '' #空字符表示成功
        #return redirect("/")  # 不能在这里返回主页,只能在html中通过这条语句返回:window.location.href = "/";
    else:
        #csrf_token = user.generate_auth_token()
        public_key_str = my_rsa.public_key_str
        return render_template('login.html',public_key_str=public_key_str, user=current_user)

@app.route("/logout")
@login_required
def logout():
    print('call logout()')
    logout_user()
    #session.pop('username',None)
    #session.pop('password',None)
    session.clear()  # 彻底删除cookie中的session
    return '' #空字符表示成功
    #return redirect("/login")
    #return redirect(url_for('login')) 不宜在接口服务器中redirect

@app.route("/update_github_user",methods=['POST'])
@login_required
def update_github_user():
    if request.method == "POST": #如果是POST方式,表示在修改页面按下了"修改"按钮.
        GitHubUserName = request.form.get('GitHubUserName')
        conn = cx_Oracle.connect(db_user, db_password, db_address)
        cur = conn.cursor()
        GitHubUserName=GitHubUserName.strip()
        if GitHubUserName != '':
            cur.execute("UPDATE is_analysis_studyinfo SET github_username=:GitHubUserName,update_date=sysdate WHERE id=:id",
                    {"GitHubUserName":GitHubUserName, "id":current_user.id})
        else: #如果没有用户名,要清空日期
            cur.execute("UPDATE is_analysis_studyinfo SET github_username=NULL ,update_date=NULL WHERE id=:id",
                    {"id":current_user.id})
        conn.commit() # 提交是必须的
        conn.close()
        check_student_url(current_user.id)
        return ''  # 空字符表示成功
        #return redirect('/') #返回主页
    #else: # 如果是GET方式访问接口,返回修改用户名的页面
        #realname, username=get_one_user(stu_id)
    #    return render_template('update.html', user=current_user)

@app.route("/update_password",methods=['POST'])
@login_required
def update_password():
    if request.method == "POST": #如果是POST方式,表示在修改页面按下了"修改"按钮.
        str_base64_password = request.form.get('encrypt_password')
        password = my_rsa.decrypt(str_base64_password)  # 用私钥解密
        generate_password = generate_password_hash(password)
        print('用私钥解密出的密码是:%s, 存储到数据库中的密码值是:%s' % (password,generate_password))
        conn = cx_Oracle.connect(db_user, db_password, db_address)
        cur = conn.cursor()
        cur.execute("UPDATE is_analysis_studyinfo SET password=:password WHERE id=:id",
                {"password":generate_password, "id":current_user.id})
        conn.commit() # 提交是必须的
        conn.close()
        return ''  # 空字符表示成功


@app.route("/grading/<string:user_id>",methods=['POST'])
@login_required
def grading(user_id):
    str_base64_password = request.form.get('encrypt_password')
    password = my_rsa.decrypt(str_base64_password)  # 用私钥解密
    generate_password = generate_password_hash(password)
    print('用私钥解密出的密码是:%s, 存储到数据库中的密码值是:%s' % (password,generate_password))
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    cur.execute("UPDATE is_analysis_studyinfo SET password=:password WHERE id=:id",
            {"password":generate_password, "id":current_user.id})
    conn.commit() # 提交是必须的
    conn.close()
    return ''  # 空字符表示成功


# 评定成绩的时候取下一个学生
@app.route("/get_next_student/<string:user_id>", methods=['GET'])
@login_required
def get_next_student(user_id):
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    cur.execute("select IS_ANALYSIS_Pack.get_next_student('%s') from dual" % user_id)
    tests = cur.fetchall()
    conn.close()
    if tests[0][0]:
        return jsonify({'success': True, 'student_id': tests[0][0]})
    else:
        return jsonify({'success': False, 'reason': '已经是最后一个'})
    #return render_template('grading_show.html', tests=tests, user=current_user)

# 评定成绩的时候取上一个学生
@app.route("/get_prev_student/<string:user_id>", methods=['GET'])
@login_required
def get_prev_student(user_id):
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    cur.execute("select IS_ANALYSIS_Pack.get_prev_student('%s') from dual" % user_id)
    tests = cur.fetchall()
    conn.close()
    if tests[0][0]:
        return jsonify({'success': True, 'student_id': tests[0][0]})
    else:
        return jsonify({'success': False, 'reason': '已经是第一个'})
    #return render_template('grading_show.html', tests=tests, user=current_user)

# 跳转到评定成绩页面
@app.route("/grading_show/<string:user_id>", methods=['GET'])
@login_required
def grading_show(user_id):
    if current_user.role == "学生" and user_id != current_user.id:
        return "不能查看别人的成绩"
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    cur.execute(
        "select student_id,test_id,result,memo,update_date,name,class,title,github_username,web_sum,result_sum from is_analysis_studytest_view where student_id=:student_id order by test_id",
        {"student_id": user_id})
    tests = cur.fetchall()
    conn.close()
    return render_template('grading_show.html', tests=tests, user=current_user)


#评定成绩
@app.route("/grading_update",methods=['POST'])
@login_required
def grading_update():
    if current_user.role == "老师":
        conn = cx_Oracle.connect(db_user, db_password, db_address)
        cur = conn.cursor()
        student_id=request.json['student_id']
        tests = request.json['tests']
        print(student_id)
        for test in tests:
            result = test['result']
            memo = test['memo']
            test_id = test['test_id']
            print("result=%s,memo=%s,student_id=%s,test_id=%s"%(result, memo, student_id, test_id))
            if result != '':
                cur.execute("update is_analysis_studytest set result=:result,memo=:memo,update_date=sysdate where student_id=:student_id and test_id=:test_id",
                    {"result": result,"memo": memo,"student_id": student_id,"test_id": test_id})
            else:
                cur.execute("update is_analysis_studytest set result=NULL,memo=:memo ,update_date=NULL where student_id=:student_id and test_id=:test_id",
                    {"memo": memo,"student_id": student_id,"test_id": test_id})
        #汇总成绩:
        cur.callproc("IS_ANALYSIS_Pack.Calc_Result_Sum",[student_id])
        conn.commit()  # 提交是必须的
        conn.close()
        return ""
    else:
        return "学生无此权限"

if __name__ == "__main__":
    print('start') #debug=True的情况下,会运行两次!
    # 必须先调用这个函数,读入密钥
    my_rsa.ReadKeyStr()
    #第二个参数是全局名称
    app.add_template_global(my_split, 'my_split')
    #使用https方式将使抓出的IP包无法直接观看.
    #app.run(host="0.0.0.0", port=1522, debug=True) # ,ssl_context='adhoc')

    WSGIServer(('0.0.0.0',1522),app).serve_forever() #异步非堵塞实现

    # make_server('0.0.0.0',1522,app).serve_forever() #异步非堵塞实现,过时了,长期运行不稳定,会报错如下:
'''    
Traceback (most recent call last):
File "C:\Python34\lib\socketserver.py", line 305, in _handle_request_noblock
self.process_request(request, client_address)
File "C:\Python34\lib\socketserver.py", line 331, in process_request
self.finish_request(request, client_address)
File "C:\Python34\lib\socketserver.py", line 344, in finish_request
self.RequestHandlerClass(request, client_address, self)
File "C:\Python34\lib\socketserver.py", line 673, in __init__
self.handle()
File "C:\Python34\lib\wsgiref\simple_server.py", line 133, in handle
handler.run(self.server.get_app())
File "C:\Python34\lib\wsgiref\handlers.py", line 144, in run
self.close()
File "C:\Python34\lib\wsgiref\simple_server.py", line 35, in close
self.status.split(' ',1)[0], self.bytes_sent
AttributeError: 'NoneType' object has no attribute 'split'
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_login import UserMixin

###从Werkzeug的模块中导入两个函数

# Flask的认证扩展
# http://blog.csdn.net/GeekLeee/article/details/52650609

class User(UserMixin):
    id = ''
    name = ''
    class_ = ''
    github_username = ''
    role = ''
    password = ''
    result_sum = ''
    web_sum=''

if __name__ == "__main__":
    u1 = User()
    u1.id = 'u1'
    u1.password = '123'
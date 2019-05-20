#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
# 加载现有配置文件
conf = configparser.ConfigParser()
conf.read("config.ini")

db_user = conf.get('config', 'db_user')
db_password = conf.get('config', 'db_password')
db_address = conf.get('config', 'db_address')
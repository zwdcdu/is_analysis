#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, jsonify, session, redirect, url_for, make_response
import requests
import cx_Oracle

from my_db import db_user,db_password,db_address

# 计算所有学生的分数汇总
def calc_result_sum_all():
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    cur.callproc("IS_ANALYSIS_Pack.Calc_Result_Sum_ALL")
    cur.close()
    conn.commit()
    conn.close()
    print("calc_result_sum_all() 执行成功.")

def check_url(url):
    code = requests.get(url).status_code
    if code == 200:
        return True
    return False

# 检测所有用户的GitHub目录是否正确
def check_student_url(student_id=None):
    conn = cx_Oracle.connect(db_user, db_password, db_address)
    cur = conn.cursor()
    sql = "SELECT count(*) FROM is_analysis_testinfo"
    cur.execute(sql)
    test_count_=cur.fetchall()
    test_count=test_count_[0][0]
    lst = []
    #test_count是实验总数的test1,test2,...testn目录是否存在,+1表示根目录是否存在
    for i in range(test_count+1):
        lst.append('N') # 初始化为不存在 N
    if student_id is None:
        cur.execute("SELECT id,github_username FROM is_analysis_studyinfo")
    else:
        cur.execute("SELECT id,github_username FROM is_analysis_studyinfo where id=:id",{"id":student_id})
    rows = cur.fetchall()
    for row in rows:
        #下面循环每个用户
        for i in range(test_count + 1):
            lst[i]='N'  # 初始化为不存在 N
        if row[1] is not None: #如果github_username存在
            url="https://github.com/%s/is_analysis" % row[1]
            if check_url(url):
                lst[0]='Y' #根目录存在
                for i in range(test_count): #测试每个实验的子目录是否存在
                    url = "https://github.com/%s/is_analysis/tree/master/test%d" % (row[1],i+1) #i从0开始的
                    if check_url(url):
                        lst[i+1]='Y' #根目录存在
        #将lst[]转化为逗号分隔的字符串
        v_web_sum = ''
        j=0
        for c in lst:
            if j == 0:
                v_web_sum=  v_web_sum+c
            else:
                v_web_sum = v_web_sum+','+c
            j = j + 1

        print("id=%s,web_sum=%s" % (row[0],v_web_sum))
        cur.execute("update is_analysis_studyinfo set web_sum=:web_sum where id=:id",{"web_sum": v_web_sum, "id": row[0]})
        conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    calc_result_sum_all()
    check_student_url()
    #check_student_url('201510511129') #周志强
    #check_student_url('201410414205')
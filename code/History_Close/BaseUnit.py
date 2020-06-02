
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:43:37 2019

@author: pengdk
"""

import pymysql
import datetime

# %% 数据库操作
#=======================================================================================================================
#新增，更新等操作
def  updateTableData(sql):
    db = pymysql.connect(
        host='192.168.1.10', port=3306,user='guest', passwd='123123',
        db='historyShot', charset='utf8')

    cur = db.cursor()
    ret = False
    try:
        cur.execute(sql)
        db.commit()
        ret = True
    except:
        db.rollback()
        ret = False
        
    cur.close()
    db.close()
    return ret

#新增，更新等操作
def updateTableData_v2(conn, sql):
    cur = conn.cursor()
    ret = False
    try:
        cur.execute(sql)
        conn.commit()
        ret = True
    except:
        conn.rollback()
        ret = False

    cur.close()
    return ret

#查询操作
def  queryTableData(sql):
    db = pymysql.connect(
        host='192.168.1.10', port=3306,user='guest', passwd='123123',
        db='historyShot', charset='utf8')
    cur = db.cursor()
    cur.execute( sql)
    ret = cur.fetchall()
    cur.close()
    db.close()
    return ret

#查询操作
def queryTableData_v2(conn, sql):
    cur = conn.cursor()
    cur.execute( sql)
    ret = cur.fetchall()
    cur.close()
    return ret

# %%基础函数
#=======================================================================================================================
#把含有千分位的字符串，转换为float
def   dotstring2float(s):
    return  float( s.replace(',' , '') )


#把datetime转换为数字形式的YYYYMMDD
def    dateToInt( dt_base ):
    return dt_base.year*10000 + dt_base.month*100 + dt_base.day





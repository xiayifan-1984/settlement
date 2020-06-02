# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:44:27 2020

@author: xiayf
"""

import os
import datetime
import codecs
import pandas as pd

def parseTrade(rootdir, dt_today, account):
    curdir = os.path.join( rootdir, "KuaiqiData")
    if not os.path.exists(curdir):
        return None

    datenum = dt_today.year*10000 + dt_today.month*100 + dt_today.day
    print(datenum)
    
    s = '{0}_Trade_{1}.csv'.format(account, datenum)
    filename = os.path.join(curdir, s)
    
    if os.path.exists(filename) and os.path.isfile(filename):
        df_txt = pd.read_csv(filename)
        return df_txt
    
    return None

def gb2312_utf8(dstdir, gb2312, utf8 ):
    #如果文件不存在
    if not os.path.exists(os.path.join(dstdir, gb2312)):
        return

    newFile = codecs.open(os.path.join(dstdir, utf8), 'w', 'utf-8')
    f = codecs.open(os.path.join(dstdir, gb2312), 'r', 'gb2312')
    newFile.write(  f.read( ) )
    f.close()
    newFile.close()
    pass

def doPreHandler(rootdir, dt_today, account):
    #文件名为"成交记录_191016.csv"， 处理成"9110000005_Trade_20191016.csv", 并把编码改为'UTF-8'
    curdir = os.path.join( rootdir, "KuaiqiData")

    src = '成交记录_{}.csv'.format(dt_today.year%100 *10000 + dt_today.month*100 + dt_today.day)
    dst = '{}_Trade_{}.csv'.format(account, dt_today.year*10000 + dt_today.month*100 + dt_today.day)

    gb2312_utf8(curdir, src, dst)

    src2 = '持仓_{}.csv'.format(dt_today.year%100 *10000 + dt_today.month*100 + dt_today.day)
    dst2 = '{}_Position_{}.csv'.format(account, dt_today.year*10000 + dt_today.month*100 + dt_today.day)
    gb2312_utf8(curdir, src2, dst2)

    pass

def main(rootdir, dt_today, account):
    doPreHandler(rootdir,dt_today,account)
    df=parseTrade(rootdir,dt_today,account)
    if df is not None:
        print(df.index)
    pass

if __name__ == '__main__':
    curfile = os.path.realpath(__file__)
    curdir = os.path.dirname( os.path.dirname(curfile) )
    rootdir = os.path.join( curdir, "sharedata")

    #dt_today = datetime.datetime.strptime("2019-10-14 15:00:00","%Y-%m-%d %H:%M:%S")
    dt_today = datetime.datetime.now()

    account = '9110000005'

    main(rootdir, dt_today, account)
    pass
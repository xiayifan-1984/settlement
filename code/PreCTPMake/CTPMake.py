# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:25:11 2019

@author: pengdk
"""

import os
import datetime
import codecs
import pandas as pd


#分析成交记录
def parseTrade(rootdir, dt_today, account):
    curdir = os.path.join( rootdir, "KuaiqiData")
    if not os.path.exists(curdir):
        return None

    datenum = dt_today.year*10000 + dt_today.month*100 + dt_today.day
    s = '{0}_Trade_{1}.csv'.format(account, datenum)
    filename = os.path.join(curdir, s)
    
    if os.path.exists(filename) and os.path.isfile(filename):
        df_txt = pd.read_csv(filename)
        return df_txt

    return None


#分析持仓记录
def parsePosition(rootdir, dt_today, account):
    curdir = os.path.join( rootdir, "KuaiqiData")
    if not os.path.exists(curdir):
        return None

    datenum = dt_today.year*10000 + dt_today.month*100 + dt_today.day
    s = '{0}_Position_{1}.csv'.format(account, datenum)
    filename = os.path.join(curdir, s)
    
    if os.path.exists(filename) and os.path.isfile(filename):
        df_txt = pd.read_csv(filename)
        return df_txt

    return None
    

def writePosition(df_txt, newFile,  datenum):
    tag_1 = '-------------------------------------------\n'
    headstr = '|品种|合约|买持|买均价|卖持|卖均价|昨结算|今结算|持仓盯市盈亏|保证金占用|投/保|多头期权市值|空头期权市值|\n'
    
    newFile.write('    持仓汇总 Positions\n')
    newFile.write( tag_1)
    newFile.write( headstr)
    newFile.write( tag_1)
    
    poslist = {}
    def lambda_pos(x):
        if len(x) ==0:
            return
        
        code = x[0]
        direction = x[1].strip()
        value = x[2]

        if code not in poslist:
            poslist[code] =[ 0, 0]

        if direction == '买':
            poslist[code][0] = value
        else:
            poslist[code][1] = value
        pass
    
    df_txt.apply(lambda_pos, axis =1)

    for code,x in poslist.items():

        #s = '|品种|{}|{}|买均价|{}|卖均价|昨结算|今结算|持仓盯市盈亏|保证金占用|投/保|多头期权市值|空头期权市值|\n'.format(
        #        code, x[0], x[1])
        
        s = '|品种|{}|{}|买均价|{}|卖均价|昨结算|今结算|持仓盯市盈亏|保证金占用|投/保|多头期权市值|空头期权市值|\n'.format(
                code, x[0], x[1])

        newFile.write(s)
        pass

    newFile.write( tag_1)
    newFile.write( tag_1)
    newFile.write( '\n\n\n\n')
    pass


def writeTrade(df_txt, newFile, datenum):
    tag_1 = '-------------------------------------------\n'
    headstr = '|成交日期|交易所|品种|合约|买/卖|投/保|成交价|手数|成交额|开平|手续费|平仓盈亏|权利金收支|成交序号|\n'

    newFile.write('     成交记录 Transaction Record\n')
    newFile.write( tag_1)
    newFile.write( headstr)
    newFile.write( tag_1)

    def lambda_trade(x):
        if len(x) ==0:
            return
        
        #s = '|{}|{}|品种|{}|{}|投保|{}|{}|成交额|{}|0|平仓盈亏|权利金收支|{}|\n'.format(
        #    datenum, x[10], x[1], x[2], x[4], x[5],x[3],x[0]   )

        s = '|{}|{}|品种|{}|{}|投保|{}|{}|成交额|{}|{}|平仓盈亏|权利金收支|{}|\n'.format(
            datenum, x['交易所'], x['合约'], x['买卖'], x['成交价格'], x['成交手数'],x['开平'],x['手续费'],x['成交编号']   )
        
        newFile.write(s)
        pass

    df_txt.apply(lambda_trade, axis = 1)

    newFile.write( tag_1)
    newFile.write( tag_1)
    newFile.write( '\n\n\n\n')
    pass


def writeFileHeader(newFile):
    newFile.write('由csv数据生成结算单\n\n\n\n')
    pass


def doTask(rootdir, dt_today, account):
    #创建新文件
    datenum = dt_today.year*10000 + dt_today.month*100 + dt_today.day
    dstdir = os.path.join(rootdir, 'datactp_jn')
    filename = '{0}_{1}.txt'.format(account, datenum)
    newFile = codecs.open(os.path.join(dstdir,filename), 'w', 'utf-8')

    #写入文件头
    writeFileHeader(newFile)

    #读取成交记录，然后写入新文件
    df = parseTrade(rootdir, dt_today, account)
    if df is not None:
        writeTrade(df, newFile, datenum)
        
    df_txt = parsePosition(rootdir, dt_today, account)
    if df_txt is not None:
        writePosition(df_txt, newFile, datenum)
        
    newFile.close()
    pass

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
    #预处理文件
    doPreHandler(rootdir, dt_today, account)
    #生成结算单
    doTask(rootdir, dt_today, account)
    pass









##############################################################################
'''

if __name__ == '__main__':
    curfile = os.path.realpath(__file__)
    curdir = os.path.dirname( os.path.dirname(curfile) )
    rootdir = os.path.join( curdir, "sharedata")

    #dt_today = datetime.datetime.strptime("2019-10-14 15:00:00","%Y-%m-%d %H:%M:%S")
    dt_today = datetime.datetime.now()

    account = '9110000005'

    main(rootdir, dt_today, account)
    pass

'''



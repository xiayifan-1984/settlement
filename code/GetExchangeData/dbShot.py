
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:39:55 2019

@author: pengdk
"""

import xlrd  #引入模块
# 导入MySQL库
import pymysql

import datetime
import re
import os
import json

import BaseUnit as BU

#=======================================================================================================================
def get_maridb(conn, tradedatestr):
    t_sql = "select * from historySnap where tradedate = '{0}' ".format(tradedatestr)
    data = BU.queryTableData_v2(conn, t_sql)
    if data:
        return [ x[1] for x in data   ]
    else:
        return None

#写入数据库
def write_maridb(re_map, tradedatestr):
    
    print("==============write_maridb")
    conn = pymysql.connect(
        host='192.168.1.10', port=3306,
        user='guest', passwd='123123',
        db='historyShot', charset='utf8',
    )

    #[1]获取所有指定date 的代码
    codelist = get_maridb(conn, tradedatestr)
        
    #[2]过滤
    new_map ={}
    for code, val in re_map.items():
        if codelist and code in codelist:   # and 的优先级低于 in
            continue
        else:
            new_map[code] = val
    
    #[3]剩下的    
    if len(new_map) >0 :
        li = []
        for code, x in new_map.items():
            s = " ('%s', '%s',  %f , %f, %f, %f, %f, %f, %f, %f) " % (tradedatestr, code, x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]  )
            li.append( s )
            
        sql = "insert into historySnap values " + ','.join( li )
        bret = BU.updateTableData_v2( conn, sql)
        if bret :
            print("success")
        else:
            print("failure")
            
    conn.close()        
    pass

# %%    
#=======================================================================================================================
class parseCZCE(object):
    def __init__(self):
        pass
    
    def doParseOne(self, filepath, isOption, remap):
    
        #打开文件，获取excel文件的workbook（工作簿）对象
        workbook=xlrd.open_workbook(filepath)
        #通过sheet索引获得sheet对象
        worksheet=workbook.sheet_by_index(0)
    
        nrows=worksheet.nrows  #获取该表总行数
        #ncols=worksheet.ncols  #获取该表总列数
        
        if isOption:
            pattern = r'^[A-Z]+\d+[CP]\d+$'
        else:
            pattern = r'^[A-Z]+\d+$'
    
        #通过坐标读取表格中的数据
        for i in range(nrows):
            code = worksheet.cell_value(i, 0)
            if bool(re.match(pattern, code)):
                realcode = code
                presettle=  BU.dotstring2float( worksheet.cell_value(i, 1) )
                openp =     BU.dotstring2float( worksheet.cell_value(i, 2) )
                highp =     BU.dotstring2float( worksheet.cell_value(i, 3) )
                lowp =      BU.dotstring2float( worksheet.cell_value(i, 4) )
                close=      BU.dotstring2float( worksheet.cell_value(i, 5) )
                settle=     BU.dotstring2float( worksheet.cell_value(i, 6) )
                volume=     BU.dotstring2float( worksheet.cell_value(i, 9) )
                amount=     BU.dotstring2float( worksheet.cell_value(i, 12) )
            
                remap[realcode] = [ presettle, openp, highp, lowp, close, settle, volume, amount ]
            else:
                continue
        
        return None

    def doParse(self, datenum, parentdir):
        remap = {}
        
        #future
        fname = 'czce_%d_f.xls' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, False, remap)
        
        #option
        fname = 'czce_%d_o.xls' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, True, remap)
        
        self._remap = remap
        pass
    
    def writeDB(self, datenum):
        write_maridb(self._remap, str(datenum) )
        pass
   

# %%
#=======================================================================================================================
class parseDCE(object):
    def __init__(self):
        kmap = {}
        kmap['豆一'] = 'a'
        kmap['豆二'] = 'b'
        kmap['胶合板'] = 'bb'
        kmap['玉米'] = 'c'
        kmap['玉米淀粉'] = 'cs'
        kmap['乙二醇'] = 'eg'
        kmap['纤维板'] = 'fb'
        kmap['铁矿石'] = 'i'
        kmap['焦炭'] = 'j'
        kmap['鸡蛋'] = 'jd'
        kmap['焦煤'] = 'jm'
        kmap['聚乙烯'] = 'l'
        kmap['豆粕'] = 'm'
        kmap['棕榈油'] = 'p'
        kmap['聚丙烯'] = 'pp'
        kmap['聚氯乙烯'] = 'v'
        kmap['豆油'] = 'y'
        
        self._kmap = kmap
        pass
    
    def doParseOne(self, filepath, isOption, remap):
        #打开文件，获取excel文件的workbook（工作簿）对象
        workbook=xlrd.open_workbook(filepath)
        #通过sheet索引获得sheet对象
        worksheet=workbook.sheet_by_index(0)
    
        nrows=worksheet.nrows  #获取该表总行数
        #ncols=worksheet.ncols  #获取该表总列数
    
        #通过坐标读取表格中的数据
        for i in range(nrows):
            code = worksheet.cell_value(i, 0)
            if code in self._kmap:
                pr = self._kmap[code]
                
                if isOption:
                    realcode = worksheet.cell_value(i, 1)
                else:
                    realcode = "{0}{1}".format( pr, worksheet.cell_value(i, 1) )
                
                presettle=     BU.dotstring2float( worksheet.cell_value(i, 6) )  
                openp =     BU.dotstring2float( worksheet.cell_value(i, 2) )
                highp =     BU.dotstring2float( worksheet.cell_value(i, 3) )
                lowp  =     BU.dotstring2float( worksheet.cell_value(i, 4) ) 
                close =     BU.dotstring2float( worksheet.cell_value(i, 5) ) 
                settle=     BU.dotstring2float( worksheet.cell_value(i, 7) )  
                volume=     BU.dotstring2float( worksheet.cell_value(i, 10) )   
                amount=     BU.dotstring2float( worksheet.cell_value(i, 13) )
            
                remap[realcode] = [ presettle, openp, highp, lowp, close, settle, volume, amount ]
            else:
                continue
        
        return None
    
    def doParse(self, datenum, parentdir):
        remap = {}
        
        #future
        fname = 'dce_%d_f.xls' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, False, remap)
        
        #option
        fname = 'dce_%d_o.xls' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, True, remap)
        
        self._remap = remap
        pass
    
    def writeDB(self, datenum):
        write_maridb(self._remap, str(datenum) )
        pass

# %%    
#=======================================================================================================================
class parseSHFE(object):
    def __init__(self):
        pass
    
    def doParse(self, datenum, parentdir):
        remap = {}
        
        #future
        fname = 'shfe_%d_f.dat' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, False, remap)
        
        #option
        fname = 'shfe_%d_o.dat' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseOne(fpath, True, remap)
        
        self._remap = remap
        pass
    
    #检查a的类型；  在本json中，本来value是一个数值型，但是数值如果为空，它又变成了''
    def ascheck(self, a):
        if isinstance(a, str):
            return 0.0
        if isinstance(a, int):
            return float(a)
        if isinstance(a, float):
            return a
        
    def doParseOne(self, filepath, isOption, remap):
        fp = open(filepath, 'r', encoding='utf-8')
        info = json.load(fp)
        
        for one in  info['o_curinstrument']:
            
            if isOption:
                realcode = one["INSTRUMENTID"].strip()
                if len(realcode) <7:
                    continue
                
            else:
                prp = one["PRODUCTID"].strip()
                if not bool( re.match(r'^[a-zA-Z]+_f$', prp) ):
                    continue
                
                pr = prp.replace("_f", "")
                month = one["DELIVERYMONTH"].strip()
                
                if not bool(re.match(r'^\d+$', month)):
                    continue
                
                realcode = pr + month
                pass
            
            presettle = self.ascheck(one["PRESETTLEMENTPRICE"])
            openp =  self.ascheck(one["OPENPRICE"])
            highp = self.ascheck(one["HIGHESTPRICE"])
            lowp = self.ascheck(one["LOWESTPRICE"])
            close = self.ascheck(one["CLOSEPRICE"])
            settle = self.ascheck(one["SETTLEMENTPRICE"])
            volume = self.ascheck(one["VOLUME"])
            amount = float(0.0)
            
            remap[realcode] = [ presettle, openp, highp, lowp, close, settle, volume, amount  ]
           
        
        fp.close()
        pass

    def writeDB(self, datenum):
        write_maridb(self._remap, str(datenum) )
        pass
   



# %%    
#=======================================================================================================================
class parseINE(object):
    def __init__(self):
        pass
    
    #检查a的类型；  在本json中，本来value是一个数值型，但是数值如果为空，它又变成了''
    def ascheck(self, a):
        if isinstance(a, str):
            return 0.0
        if isinstance(a, int):
            return float(a)
        if isinstance(a, float):
            return a
            
    def doParse(self, datenum, parentdir):
        remap = {}
        
        #future
        fname = 'ine_%d_f.dat' % (datenum)
        fpath = os.path.join(parentdir, fname)
        self.doParseFuture(fpath, remap)
        
        self._remap = remap
        pass

    def doParseFuture(self, filepath, remap):
        fp = open(filepath, 'r', encoding='utf-8')
        info = json.load(fp)

        for one in  info['o_curinstrument']:
            #代码由2部分组成，一部分是Product, 一部分是月份
            prp = one["PRODUCTID"].strip()
            if not bool( re.match(r'^[a-zA-Z]+_f$', prp) ):
                continue
                
            pr = prp.replace("_f", "")
            month = one["DELIVERYMONTH"].strip()
                
            if not bool(re.match(r'^\d+$', month)):
                continue
                
            realcode = pr + month
            #行情数据
            presettle = self.ascheck(one["PRESETTLEMENTPRICE"])
            openp =  self.ascheck(one["OPENPRICE"])
            highp = self.ascheck(one["HIGHESTPRICE"])
            lowp = self.ascheck(one["LOWESTPRICE"])
            close = self.ascheck(one["CLOSEPRICE"])
            settle = self.ascheck(one["SETTLEMENTPRICE"])
            volume = self.ascheck(one["VOLUME"])
            amount = float(0.0)

            remap[realcode] = [ presettle, openp, highp, lowp, close, settle, volume, amount  ]
            pass

        fp.close()
        pass

    def writeDB(self, datenum):
        write_maridb(self._remap, str(datenum) )
        pass

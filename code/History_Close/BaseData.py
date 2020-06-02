# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:28:34 2019

@author: pengdk
"""

import BaseUnit as BU
import datetime
import re

# %%
#=======================================================================================================================
# 节假日有关的操作
class CHolidayData(object):
    def __init__(self):
        data = BU.queryTableData( "select * from chinaholiday" )
        if data:
            self._holiday = [ x[1] for x in data ]
        else: 
            self._holiday = [ ]
        pass
    
    #base_dt是否为工作日
    def isWorkDay(self, base_dt):
        dt = base_dt

        if dt.weekday() ==5 or dt.weekday() == 6:
            return False
        
        num = BU.dateToInt( dt ) 
        if num in self._holiday:
            return False
        
        return True
    
    #base_dt向前找一个工作日
    def preWorkDay(self, base_dt):
        dt = base_dt
        
        count = 100
        while count >0:
            count -= 1
            dt = dt +datetime.timedelta(days = -1)
            if self.isWorkDay( dt ):
                return dt
            pass
            
        return None

    #base_dt向后找一个工作日
    def postWorkDay(self, base_dt):
        dt = base_dt
        
        count = 100
        while count >0:
            count -= 1
            
            dt = dt +datetime.timedelta(days = 1)
            
            if self.isWorkDay( dt ):
                return dt
            pass
        
        return None


    #计算剩余天数(从dt_today开始，计算到enddate中间的工作日，算尾不算头)
    def calcLeftDays(self, enddate, dt_today):
        num =0
        
        dt = dt_today
        start = BU.dateToInt( dt )
        end = BU.dateToInt( enddate ) 
        
        while start < end:
            dt = dt + datetime.timedelta(days=1)
            start = BU.dateToInt( dt )
            
            if self.isWorkDay( dt ):
                num += 1
                
            pass
        
        return num
    
    #计算从start_dt到end_dt 之间的工作日， (算尾不算头)
    def getWorklist(self, start_dt, end_dt):
        dt = start_dt
        start = BU.dateToInt( dt ) 
        end = BU.dateToInt( end_dt ) 
        
        worklist = []
        while start < end:
            dt = dt + datetime.timedelta(days=1)
            start = BU.dateToInt( dt ) 
            
            if self.isWorkDay(dt):
                worklist.append(dt)
                
            pass
        
        return worklist


# %%
#=======================================================================================================================
class CProductData(object):
    def __init__(self):
        self.init_multiple()
        pass

    def init_multiple(self):
        data = BU.queryTableData( "select code, multi, exchange from product" )
        if data:
            self._vmmap = { x[0]:[ x[1], x[2] ] for x in data }
        else:
            self._vmmap = {}
        pass

    def getMultiple(self, code):
        product = self.getProductByCode(code)
        if product in self._vmmap:
            return self._vmmap[product][0]
        else:
            err = "错误:无法获取合约乘数，请检查 {0} and {1} not in vmmap".format( code, product)
            raise Exception(err)
        
        return 0

    def getExchange(self, code):
        product = self.getProductByCode(code)
        if product in self._vmmap:
            return self._vmmap[product][1]
        else:
            err = "错误:无法获取交易所，请检查 {0} and {1} not in vmmap".format( code, product)
            raise Exception(err)
        
        return ""

    def getUnderlyingByOptioncode(self, optioncode):
        underlyingcode = re.match(r'\D+\d+', optioncode).group()
        return underlyingcode
    
    def getProductByCode(self, code):
        if len(code) < 8:   #如果是期货
            product = re.match(r'\D+', code).group()
            return product
        
        else:       #如果是期权
            if bool(re.match(r'^m\d+-[CP]-\d+$', code)):
                product = 'm_o'
            elif bool(re.match(r'^c\d+-[CP]-\d+$', code)):
                product = 'c_o'
            elif bool(re.match(r'^cu\d+[CP]\d+$', code)):
                product = 'cu_o'
            elif bool(re.match(r'^ru\d+[CP]\d+$', code)):
                product = 'ru_o'
            elif bool(re.match(r'^CF\d+C\d+$', code)):
                product = 'CFC'
            elif bool(re.match(r'^CF\d+P\d+$', code)):
                product = 'CFP'
            elif bool(re.match(r'^SR\d+C\d+$', code)):
                product = 'SRC'
            elif bool(re.match(r'^SR\d+P\d+$', code)):
                product = 'SRP'
            elif bool(re.match(r'^i\d+-[CP]-\d+$', code)):
                product = 'i_o'
            else:
                product = ""
                raise Exception('无法获取期权的品种，请检查')
                
            return product
        
        return ""


# %%
#=======================================================================================================================
class CSnapData(object):
    def __init__(self, dt):
        self.init_snap(dt)
        pass
    
    def init_snap(self, dt):
        sql = '''
        SELECT A.tradedate, A.CODE, A.close, A.settle FROM historySnap A 
        WHERE A.tradedate = '{0}'
        '''.format( BU.dateToInt( dt ) )

        data = BU.queryTableData(sql)
        if data:
            self._pricemap = { x[1]: [ x[2], x[3] ] for x in data  }
        else:
            self._pricemap = { }
        pass

    def getClosePrice(self, code):
        if code in self._pricemap:
            return self._pricemap[code][0]
        else:
            err = "[无法取得 {0} 的收盘价,默认为0]".format(code) 
            raise Exception(err)

        return 0.0

    def getSettlePrice(self, code):
        if code in self._pricemap:
            return self._pricemap[code][1]
        else:
            err = "[无法取得 {0} 的结算价,默认为0]".format(code) 
            raise Exception(err)

        return 0.0



class CSnapData4(object):
    def __init__(self, dt_today, dt_preworkday):
        self._dt_today = dt_today
        self._dt_preworkday = dt_preworkday
        pass
        
    def start(self):
        self.init_snap()
        pass
        
    def init_snap(self):
        dt_base = self._dt_today
        dt_pre = self._dt_preworkday
        
        today =  BU.dateToInt( dt_base )
        preday = BU.dateToInt( dt_pre ) 
        
        sql = '''
            SELECT A.tradedate, A.CODE, A.close, A.presettle, A.settle, B.close AS preclose 
            FROM historySnap A,(SELECT CODE, close FROM historySnap WHERE tradedate = '{0}') AS B
            WHERE A.tradedate = '{1}' AND A.CODE = B.CODE
            '''.format( preday, today)

        print(sql)
        data = BU.queryTableData(sql)
        if not data:
            return None
        
        pricemap = { x[1]: [x[5], x[2], x[3], x[4] ] for x in data  }
        
        '''
        重整数据:
        昨结算如果为0， 等于今结算
        今收盘价如果为0， 等于今结算
        昨收盘价如果为0， 等于昨结算
        '''
        
        for _,v in pricemap.items():
            if v[2] < 0.0001:
                v[2] = v[3]
            if v[1] < 0.0001:
                v[1] = v[3]
            if v[0] < 0.0001:
                v[0] = v[2]
            pass
    
        self._pricemap = pricemap
        pass
        
    
    def getAllPrice(self, code):
        if code in self._pricemap:
            return self._pricemap[code]
        else:
            err = "错误:无法获取结算价，请检查 {0} not in _pricemap".format( code)
            raise Exception(err)
        
        return [0.0, 0.0, 0.0, 0.0]
    
    
    def getSettlePrice(self, code):
        if code in self._pricemap:
            return (self._pricemap[code][2], self._pricemap[code][3] )
        else:
            err = "错误:无法获取结算价，请检查 {0} not in _pricemap".format( code)
            raise Exception(err)
        
        return (0, 0)
    
    def getClosePrice(self, code):
        if code in self._pricemap:
            return (self._pricemap[code][0], self._pricemap[code][1] )
        else:
            err = "错误:无法获取收盘价，请检查 {0} not in _pricemap".format( code)
            raise Exception(err)
        
        return (0.0, 0.0)
    
    
    
    
    
    
    
    



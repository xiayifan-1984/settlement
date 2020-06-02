# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:27:38 2019

@author: pengdk
"""
from WindPy import *
import re

#=======================================================================================================================
#=======================================================================================================================
#获取万得中期权的Greek数据(实时)
class WindGreekData(object):
    def __init__(self):
        self._w = w
        pass
    
    def start(self):
        self._w.start()
        
    def stop(self):
        self._w.stop()
        
    def getGreekData(self, code, exchange):

        field ="rt_imp_volatility,rt_delta,rt_gamma,rt_vega,rt_theta,rt_rho"
        
        if exchange == 'SHFE':
            data = self._w.wsq(code+".SHF", field)
        elif exchange == 'CZCE':
            data = self._w.wsq(code+".CZC", field)
        elif exchange == 'DCE':
            data = self._w.wsq(code+".DCE", field)
        
        return data

#获取万得中“期权”的历史Greek数据
class WindGreekDataHistory(object):
    def __init__(self, somedate):
        self._w = w
        self._somedate = somedate
        pass
    
    def start(self):
        self._w.start()
        
    def stop(self):
        self._w.stop()
        
    def getGreekData(self, code, exchange):
        field ="us_impliedvol,delta,gamma,vega,theta,rho"
        dt = self._somedate
        begindate = "{}-{}-{}".format(dt.year, dt.month, dt.day)
        enddate = begindate
        
        if exchange == 'SHFE':
            data = self._w.wsd(code+".SHF", field, begindate, enddate)
        elif exchange == 'CZCE':
            data = self._w.wsd(code+".CZC", field, begindate, enddate)
        elif exchange == 'DCE':
            data = self._w.wsd(code+".DCE", field, begindate, enddate)
        
        return data

#=======================================================================================================================
#=======================================================================================================================
#获取万得中期权 的最后到期日 数据
class WindCUOptionData(object):
    def __init__(self):
        self._w = w
        self.codemap = { }      # key = code,  value = expire_date
        pass        
    
    def start(self):
        self._w.start()
        self.initdata('SHFE', 'CU')
        self.initdata('SHFE', 'RU')
        self.initdata('CZCE', 'CF')
        self.initdata('DCE', 'I')
        pass

    def stop(self):
        self._w.stop()
        pass
    
    #默认获取当前正在交易的所有期权合约
    def initdata(self, exchange, sub_product):
        qstr = "exchange={};productcode={};contract=all;field=wind_code,listed_date,expire_date".format(exchange, sub_product)
        data = self._w.wset("optionfuturescontractbasicinfo", qstr)
        
        if data.ErrorCode != 0:
            print("GetWindData Error ===========")
        else:
            print(data)
            
            size = len(data.Codes)
            for i in range(size):
                code = data.Data[0][i]          #str
                expire = data.Data[2][i]        #datetime.datetime
                
                self.codemap[code] = expire
                pass
            
            print("---------------------->>>>")
            print( type(data.Fields) )
            print( type(data.Codes ) )
            print( type(data.Data ))
        
        pass
    
    #请求某个标的的铜期权
    def initcustomdata(self, optioncode, exchange):
        print("====== initcustomdata ", optioncode, exchange)
        # w.wset("optionfuturescontractbasicinfo","exchange=SHFE;productcode=CU;contract=CU1909.SHF;field=wind_code,listed_date,expire_date")
        
        #获取标的代码
        underlyingcode = re.match(r'\D+\d+', optioncode).group()
        underlyingcode = underlyingcode.upper()
        #获取productCode
        productcode = re.match(r'\D+', optioncode).group()
        productcode = productcode.upper()

        if exchange == 'SHFE':
            field = "exchange=SHFE;productcode={};contract={}.SHF;field=wind_code,listed_date,expire_date".format(
                productcode, underlyingcode)
        elif exchange == 'CZCE':
            field = "exchange=SHFE;productcode={};contract={}.CZC;field=wind_code,listed_date,expire_date".format(
                productcode, underlyingcode)
        elif exchange == 'DCE':
            field = "exchange=DCE;productcode={};contract={}.DCE;field=wind_code,listed_date,expire_date".format(
                productcode, underlyingcode)

        data = self._w.wset("optionfuturescontractbasicinfo", field)
        
        if data.ErrorCode != 0:
            print("GetWindData Error ===========")
        else:
            print(data)
            
            size = len(data.Codes)
            for i in range(size):
                code = data.Data[0][i]          #str
                expire = data.Data[2][i]        #datetime.datetime
                
                self.codemap[code] = expire
                pass
        
        
        pass
    
    def compareLastdate(self, optioncode, dt_today):
        if optioncode in self.codemap:
            dt_expire = self.codemap[optioncode]
            date1 = dt_expire.year*10000 + dt_expire.month*100 + dt_expire.day
            date2 = dt_today.year*10000 + dt_today.month*100 + dt_today.day
            if date1 == date2:
                return True
            else:
                return False
            
        return False
        
    def isOptionLastdate(self, code, dt_today, exchange):
        
        optioncode = code.upper()
        if optioncode in self.codemap:
            return self.compareLastdate( optioncode, dt_today)
        else:
            self.initcustomdata(optioncode, exchange)
            #再调用compareLastdate
            return self.compareLastdate( optioncode, dt_today)
        
        return False


#=======================================================================================================================
#=======================================================================================================================










#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
'''
def testcase2():
    obj = WindCUOptionData()
    obj.start()
    
    obj.initcustomdata('CU1909c43000')
    
    pass


def testcase():
    obj = WindGreekData()
    
    obj.start()
    
    code = 'cu1909C49000.SHF'
    data = obj.getGreekData(code)
    
    print(data)
    pass
'''

if __name__ == '__main__':
    testcase2()
    
    pass
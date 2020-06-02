# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:39:55 2019

@author: pengdk
"""

from bs4 import BeautifulSoup
from lxml import html
import requests

import os

# %%
#思路是:发送get方法，URL中带有日期，获得xls文件
#=======================================================================================================================
class downCZCE(object):
    def __init__(self):
        pass
    
    def doDown(self, datenum, parentdir):
        self._datenum = datenum
        self._parentdir = parentdir
        
        self.doFuture()
        self.doOption()
        pass
    
    def doFuture(self):
        #url = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/2019/20190809/FutureDataDaily.xls"
        
        year = int(self._datenum/10000)
        root_url = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/"
        sub_url = "{0}/{1}/FutureDataDaily.xls".format( year, self._datenum )
        
        url = root_url + sub_url
    
        html = requests.get(url)
    
        opath = os.path.join(self._parentdir, "czce_%d_f.xls" %(self._datenum ) )
        with open(opath, 'w+b') as f:
            f.write(html.content)
    
        pass

    def doOption(self):
        #url = "http://www.czce.com.cn/cn/DFSStaticFiles/Option/2019/20190809/OptionDataDaily.xls"
        
        year = int(self._datenum/10000)
        root_url = "http://www.czce.com.cn/cn/DFSStaticFiles/Option/"
        sub_url = "{0}/{1}/OptionDataDaily.xls".format( year, self._datenum )
        
        url = root_url + sub_url
    
        html = requests.get(url)
        
        opath = os.path.join(self._parentdir, "czce_%d_o.xls" %(self._datenum ) )
        with open(opath, 'w+b') as f:
            f.write(html.content)
    
        pass

# %%
#思路是:发送post方法带参数， 下载xls文件
#=======================================================================================================================
class downDCE(object):
    def __init__(self):
        
        pass
    
    def doDown(self, datenum, parentdir):
        self._datenum = datenum
        self._parentdir = parentdir
        
        self.doFuture()
        self.doOption()
        pass
    
    def doFuture(self):
        date_num = self._datenum
        year, month, day = date_num/10000, (date_num%10000)/100,  date_num%100
        
        url = 'http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html'
    
        #post 的数据
        data = {
            'day': "%02d" %(day), 
            'dayQuotes.trade_type':'0', 
            'dayQuotes.variety':'all', 
            'exportFlag':'excel', 
            'month': "%d" % (month-1),
            'year': "%d" % (year) 
            }
    
        #HTTP Post方法
        html = requests.post(url, data)
        opath = os.path.join(self._parentdir, "dce_%d_f.xls" %(date_num) )
        with open(opath, 'w+b') as f:
            f.write(html.content)
        
        pass

    def doOption(self):
        date_num = self._datenum
        year, month, day = date_num/10000, (date_num%10000)/100,  date_num%100
    
        url = "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html"
    
        #post 的数据
        data = {
            'day': "%02d" %(day), 
            'dayQuotes.trade_type':'1', 
            'dayQuotes.variety':'all', 
            'exportFlag':'excel', 
            'month': "%d" % (month-1),
            'year': "%d" % (year) 
            }
    
        #HTTP Post方法
        html = requests.post(url, data)
        opath = os.path.join(self._parentdir, "dce_%d_o.xls" %(date_num) )
        with open(opath, 'w+b') as f:
            f.write(html.content)

        pass


# %%
#思路是:发送get方法，URL中带有日期，获得JSON文件
#=======================================================================================================================
class downSHFE(object):
    def __init__(self):
        pass
    
    def doDown(self, datenum, parentdir):
        self._datenum = datenum
        self._parentdir = parentdir
        
        self.doFuture()
        self.doOption()
        pass
    
    def doFuture(self):
        #url = "http://www.shfe.com.cn/data/dailydata/kx/kx20190808.dat"
        
        url = 'http://www.shfe.com.cn/data/dailydata/kx/' + "kx{0}.dat".format( self._datenum )
        html = requests.get(url)
        opath = os.path.join(self._parentdir, "shfe_%d_f.dat" %(self._datenum ) )
        with open(opath, 'w+b') as f:
            f.write(html.content)
    
        pass

    def doOption(self):
        #url = "http://www.shfe.com.cn/data/dailydata/option/kx/kx20190809.dat"
        
        url = 'http://www.shfe.com.cn/data/dailydata/option/kx/' + "kx{0}.dat".format( self._datenum )
        html = requests.get(url)
        opath = os.path.join(self._parentdir, "shfe_%d_o.dat" %(self._datenum ) )
        with open(opath, 'w+b') as f:
            f.write( html.content )

        pass

# %%
#=======================================================================================================================
#思路和上期所基本一致，只是URL有变化
#=======================================================================================================================
class downINE(object):
    def __init__(self):
        pass
    
    def doDown(self, datenum, parentdir):
        self._datenum = datenum
        self._parentdir = parentdir
        
        self.doFuture()
        self.doOption()
        pass

    def doFuture(self):
        #url = "http://www.ine.cn/data/dailydata/kx/kx20191023.dat"
        
        url = 'http://www.ine.cn/data/dailydata/kx/' + "kx{0}.dat".format( self._datenum )
        html = requests.get(url)
        opath = os.path.join(self._parentdir, "ine_%d_f.dat" %(self._datenum ) )
        with open(opath, 'w+b') as f:
            f.write(html.content)
    
        pass

    def doOption(self):
        #当前 能源中心 无期权上市
        pass

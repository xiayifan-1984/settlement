# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:39:55 2019

@author: pengdk
"""


import  os
import  datetime

import  downExch
import  dbShot

import  BaseData  as BD


# %%
#=======================================================================================================================
def main_only_download(curdir, dt):
    #日期(数字型)
    datenum = dt.year*10000 + dt.month*100 + dt.day
    
    #郑商所 下载today日期的数据到curdir
    czce = downExch.downCZCE()
    czce.doDown( datenum, curdir)
    
    #上期所
    shfe = downExch.downSHFE()
    shfe.doDown( datenum, curdir)
    
    #大商所
    dce = downExch.downDCE()
    dce.doDown( datenum, curdir)

    #上海能源中心
    # 我发现上期所的内容里面，已经包含了 INE的内容
    #ine = downExch.downINE()
    #ine.doDown( datenum, curdir)
    pass    


def updateEveryDay(curdir, dt):
    #日期(数字型)
    datenum = dt.year*10000 + dt.month*100 + dt.day
    
    #郑商所 分析+入库
    czce = dbShot.parseCZCE()
    czce.doParse( datenum, curdir)
    czce.writeDB( datenum )
    
    #大商所
    dce = dbShot.parseDCE()
    dce.doParse( datenum, curdir)
    dce.writeDB( datenum )
        
    #上期所
    shfe = dbShot.parseSHFE()
    shfe.doParse( datenum, curdir)
    shfe.writeDB( datenum )

    #上海能源中心
    #ine = dbShot.parseINE()
    #ine.doParse( datenum, curdir)
    #ine.writeDB( datenum )
    pass

def main_batch():
    #目标目录
    curfile = os.path.realpath(__file__)
    rootdir = os.path.dirname( os.path.dirname(curfile) )
    curdir = os.path.join(rootdir, "sharedata\\MarketData")

    #dt = datetime.datetime.strptime("2019-09-06 15:00:00","%Y-%m-%d %H:%M:%S")
    
    #节假日
    oholiday = BD.CHolidayData()
    
    #指定一段时间，再获取这一段时间的工作日，然后逐日下载
    start = datetime.datetime(2019, 12, 30)
    end = datetime.datetime(2019, 12, 31)
    dt_list = oholiday.getWorklist(start, end)
    
    for dt in dt_list:
        #下载
        main_only_download(curdir, dt)
    
        #更新
        #updateEveryDay(curdir, dt)
        #print("update one ======")
        
    print("main_batch end!!")
    pass

def main():
    #目标目录
    curfile = os.path.realpath(__file__)
    rootdir = os.path.dirname( os.path.dirname(curfile) )
    curdir = os.path.join(rootdir, "sharedata\\MarketData")

    #日期
    #dt = datetime.datetime.strptime("2019-10-11 15:00:00","%Y-%m-%d %H:%M:%S")
    dt = datetime.datetime.now()
    
    #下载
    main_only_download(curdir, dt)
    
    #更新
    updateEveryDay(curdir, dt)
    
    print("main end")
    pass


# %%
if __name__ == "__main__":
    #main()
    main_batch()
    pass
    
    
    
    
    
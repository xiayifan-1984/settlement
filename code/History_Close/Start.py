

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:49:18 2019

@author: pengdk
"""

import  datetime
import  os

import  HistoryOTCClose
import  HistoryCtpjnClose
import  BaseData  as BD



def main_batch():
    curfile = os.path.realpath(__file__)
    curdir = os.path.dirname( os.path.dirname(curfile) )
    rootdir = os.path.join( curdir, "sharedata")

    #节假日
    oholiday = BD.CHolidayData()
    
    #指定一段时间，再获取这一段时间的工作日，然后逐日执行
    start = datetime.datetime(2019, 4, 30)
    end = datetime.datetime(2019, 6, 1)
    dt_list = oholiday.getWorklist(start, end)
    for dt in dt_list:
        HistoryOTCClose.main(rootdir, dt )
        HistoryCtpjnClose.main(rootdir, dt )
        pass

    pass


def main():
    curfile = os.path.realpath(__file__)
    curdir = os.path.dirname( os.path.dirname(curfile) )
    rootdir = os.path.join( curdir, "sharedata")
    
    ###########################################
    #TODO
    #指定日期
    #dt_today = datetime.datetime.strptime("2019-05-14 15:00:00","%Y-%m-%d %H:%M:%S")
    dt_today = datetime.datetime.now()
    #TODO
    ############################################
    
    HistoryOTCClose.main(rootdir, dt_today )
    HistoryCtpjnClose.main(rootdir, dt_today )
    pass



if __name__ == '__main__':
    #main_batch()
    main()
    pass




# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:25:11 2019

@author: pengdk
"""


import  os
import  datetime
import  CTPMake


def main():
    curfile = os.path.realpath(__file__)
    curdir = os.path.dirname( os.path.dirname(curfile) )
    rootdir = os.path.join( curdir, "sharedata")

    #dt_today = datetime.datetime.strptime("2019-10-14 15:00:00","%Y-%m-%d %H:%M:%S")
    dt_today = datetime.datetime.now()

    #account = '9110000005'
    account = '8001888888'
    #account = '9110000002'

    CTPMake.main(rootdir, dt_today, account)
    pass



if __name__ == '__main__':
    print("main begin!!")
    main()
    print("main end!!")
    pass



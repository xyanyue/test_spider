#!/usr/bin/env python3
# -*- coding:utf-8 -*-


#######请不要直接运行谢谢##########
#######本实例是测试所写，由此产生的法律问题请自行承担#############


import sys
import spider_class

LevelName = ['first','second','three','four','five']
firstUrl = "https://m.haodf.com/touch/province/listxxxxxxxxxxx.htm"

s = spider_class.Spider(firstUrl=firstUrl, LevelName=LevelName)
# s = spider_class.Spider(back=True, LevelName=LevelName)
s.start()



            

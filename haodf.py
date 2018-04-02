#!/usr/bin/env python3
# -*- coding:utf-8 -*-



import sys
import spider_class

LevelName = ['first','second','three','four','five']
firstUrl = "https://m.haodf.com/touch/province/list.htm"

s = spider_class.Spider(firstUrl=firstUrl, LevelName=LevelName)
# s = spider_class.Spider(back=True, LevelName=LevelName)
s.start()



            
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
from conn import mysql_pool 
import sys
import pymysql
# import json
####test#####
import spider_tool
from bs4 import BeautifulSoup
import urllib
####test#####


#####这个是一个mysql的线程池是线程安全
#如果要用本身的pymysql 我不建议啊 太难弄了
m = mysql_pool.MysqlPool('Local')


#### 所要url插入表中
def insertQueue(self,url,level,t_name='test'):
    if self is not None:
        self.putQueue(url,level)
    sql = "insert into spider_url_list(url,level) values(%s,%s)"
    m.insert(sql,(url,level))

####修改表中url的状态
def updateUrlListStatus(self,url,t_name='test'):
    sql = "update spider_url_list set status=1 where url=%s"
    m.insert(sql,(url,))

##插入数据库 存在修改 不存在插入
def insertHospitalAndUpdate(self,data,hospital_name,t_name='test',tableName='haodf_base_hospital'):

    hospital_name = hospital_name.strip()
    hospital_name = hospital_name.replace('%','%%')
    hospital_name = pymysql.escape_string(hospital_name)
    print(hospital_name)
    ##将字典None转成空字符串
    data = dict(zip(list(data.keys()),list(map((lambda x:pymysql.escape_string(x.strip().replace('%','%%')) if x is not None else ''),data.values()))))

    sql = "select id from "+tableName+" where hospital_name=%s"
    res = m.fetchone(sql,(hospital_name,))
    if res :
        d = ','.join( [ k+"='"+v+"'" for k,v in data.items()])
        sql2 = "update "+tableName+" set "+d+" where hospital_name=%s"
        m.update(sql2,(hospital_name,))
    else:
        
        sql2 = "insert into "+tableName+"(hospital_name,"
        key =  ','.join( [ k for k in data.keys()])
        value =  ','.join( [ "'"+v+"'" for v in data.values()])
        
        sql2 = sql2 + key +") values(%s,"+value+")"
        # print(sql2)
        m.insert(sql2,(hospital_name,))

    
##插入数据库 存在修改 不存在插入
def insertAllAndUpdate(self,data,where,t_name='test',tableName='haodf_base_hospital'):
    
    where = dict(zip(list(where.keys()),list(map((lambda x:pymysql.escape_string(x.strip().replace('%','%%')) if x is not None else ''),where.values()))))
    ##将字典None转成空字符串
    data = dict(zip(list(data.keys()),list(map((lambda x:pymysql.escape_string(x.strip().replace('%','%%')) if x is not None else ''),data.values()))))
    


    where_str = ' and '.join( [ k+"='"+v+"'" for k,v in where.items()])

    sql = "select id from "+tableName+" where "+where_str
    res = m.fetchone(sql,())
    if res :
        d = ','.join( [ k+"='"+v+"'" for k,v in data.items()])
        sql2 = "update "+tableName+" set "+d+" where "+where_str
        m.update(sql2,())
    else:
        
        # data = dict(data.items() | where.items())
        data = dict(data,**where)
        sql2 = "insert into "+tableName+"("
        key =  ','.join( [ k for k in data.keys()])
        value =  ','.join( [ "'"+v+"'" for v in data.values()])
        
        sql2 = sql2 + key +") values("+value+")"
        # print(sql2)
        m.insert(sql2,())
    
'''

以下方法是必须实现的方法，就是根据levelName去命名的

'''

####地区页面
def result_user_first(self,url,level,soup,t_name,*,param={}):
    print(level,t_name,url)
    lilist = soup.findAll('li')
    for x in lilist:
        insertQueue(self,x.a['href'],'second',t_name)

###医院列表
def result_user_second(self,url,level,soup,t_name,*,param={}):
    pass

###医院详细信息 以及科室列表
def result_user_three(self,url,level,soup,t_name,*,param={}):
    pass
    




def result_user_four(self,url,level,soup,t_name,*,param={}):
    pass

# def before_user_five(self,url,level,t_name,*,param={}):
#     ##https://m.haodf.com/touch/faculty/loaddoctors/DE4roiYGYZwWGX0voi5u5tiO7?p=19
#     #https://m.haodf.com/touch/faculty/DE4roiYGYZwWGX0voi5u5tiO7.htm|hospital_name
#     # urlp = urllib.parse.urlparse(url)
#     urls = url.split('|')
#     url = urls[0]
#     hospital_name = urls[1]
#     u = url.replace('https://m.haodf.com/touch/faculty/','').replace('.htm','')
#     url = "https://m.haodf.com/touch/faculty/loaddoctors/"+u
#     page = 0
#     while True:
#         Html = self.runUrl(url+"?p="+str(page))
#         if Html :
#             ret = json.loads(data)
#             if ret :


    # return True,'json',url,{'hospital_name':hospital_name}

def result_user_five(self,url,level,soup,t_name,*,param={}):
    pass




if __name__ == '__main__':
    _Headers = {
                        'Accept-Language':'zh-CN,zh;q=0.9',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'User-Agent':spider_tool.Tool.randAgent()
                }

    url = "https://m.haodf.com/touch/hospital/DE4r0Fy0C9Luw0Cp0J3FS0Wg66K2nYytQ.htm"
    data = urllib.parse.urlencode({}).encode(encoding='UTF8')
    req = urllib.request.Request(url, data, _Headers)
    html = urllib.request.urlopen(req).read()
    
    level = "three"
    soup = BeautifulSoup(html,'lxml')
    result_user_three(None,url,level,soup,'test')


    ##https://m.haodf.com/touch/faculty/DE4r0Fy0C9LuGYyrs7reTNReozGolC54J.htm


















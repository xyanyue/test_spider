#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
from conn import mysql_pool 
import sys
# import pymysql
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
    


    where_str = ' and '.join( [ k+"='"+v+"'" for k,v in data.items()])

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
    print(level,t_name,url)
    list_ = soup.findAll(name='ul',attrs={"class":"dis_n_list_area"})
    prov = soup.find(name='div',attrs={"class":"head_tit"}).string.replace('地区医院','')

    for x3 in list_:
        hospital_type = x3.find_previous_sibling(name='div',attrs={"class":"hos_bj"}).string
        for x4 in x3.findAll(name='li'):
            u = x4.a['href']
            insertQueue(self,"https:"+u,'three',t_name)
            hs = x4.find_all('p')

            hospital_name = hs[0].string
            hospital_other = hs[1].string.split()
            hospital_area = hospital_other[0] if (len(hospital_other) >= 1) else ''
            hospital_level = hospital_other[1] if (len(hospital_other) >= 2) else ''

            data = {
                'area_p':prov,
                'area_c':hospital_area,
                'hospital_leixing':hospital_type,
                'hospital_dengji':hospital_level
            }
            insertHospitalAndUpdate(self,data,hospital_name,t_name)
    updateUrlListStatus(self,url,t_name)

###医院详细信息 以及科室列表
def result_user_three(self,url,level,soup,t_name,*,param={}):
    print(level,t_name,url)
    tel_replace = ['<span class="tel">','</span','<p class="hos-tel fl clearfix">','</p>',' ',"\n"]
    hospital_name = soup.find(name='div',attrs={"class":"hos-name"}).p.string

    doctor_num = soup.find(name='p',attrs={"class":'doctor-num'})
    if doctor_num is not None:
        doctor_num = doctor_num.i.string
    depart_num = soup.find(name='p',attrs={"class":'Depart-num'})
    if depart_num is not None:
        depart_num = depart_num.i.string

    hos_add = soup.find(name='p',attrs={"class":'hos-add'})
    if hos_add is not None:
        hos_add = hos_add.string
    
    hos_tel = soup.find(name='p',attrs={"class":'hos-tel'})
    if hos_tel is not None:
        hos_tel = str(hos_tel)
        if hos_tel:
            for rep in tel_replace:
                hos_tel = hos_tel.replace(rep,'')

    # print(hos_tel.strip())
    data = {
        'doc_num':doctor_num,
        'class_num':depart_num,
        'address':hos_add,
        'phone':hos_tel
    }
    print(data)
    insertHospitalAndUpdate(self,data,hospital_name,t_name)
   

    intro_url = soup.find(name='a',attrs={"id":'HospitalIntroduction_more'})
    if intro_url is not None:
        pass
        # insertQueue(self,intro_url['href'],'four',t_name)


    depart_list = soup.findAll(name='ul',attrs={"class":"depart-list"})
    for x in depart_list:
        first_level = x.find(name='li',attrs={"class":'first-level'}).string
        depart_item = x.findAll(name='li',attrs={"class":'faculty_list_cnzz'})
        for x2 in depart_item:
            depart = x2.a.span.string
            depart_url = x2.a['href']
            # insertQueue(self,depart_url,'five',t_name)
            depart_num = x2.a.i.string
            d={
                'parent_depart':first_level,
                'depart':depart,
                'num':depart_num,
            }
            w = {
                'hospital_name':hospital_name,
                'depart':depart
            }
            insertAllAndUpdate(self,d,w,t_name,'haodf_hospital_depart')
            # print(d)
    updateUrlListStatus(self,url,t_name)




def result_user_four(self,url,level,soup,t_name,*,param={}):
    print(level,t_name,url)
    hospital_name = soup.find(name='p',attrs={"class":"hos_intro"}).string.replace('简介','')
    intro = soup.find(name='p',attrs={'class':'gray6'}).get_text()
    # print(str(intro))
    intro = intro.replace('%','%%')
    insertHospitalAndUpdate(self,{'intro':intro},hospital_name,t_name)
    updateUrlListStatus(self,url,t_name)

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
    print(level,t_name,url)
    hospital_name = soup.find(name='a',attrs={'id':'cnzz_mianbao_hospital'}).string
    depart = soup.find(name='a',attrs={'id':'cnzz_mianbao_faculty'}).string
    # depart = hospital_depart[1]
    his_url = url
    u = url.replace('https://m.haodf.com/touch/faculty/','').replace('.htm','')
    url = "https://m.haodf.com/touch/faculty/loaddoctors/"+u
    page = 0
    flag = True
    where = {'hospital_name':hospital_name,'depart':depart}
    while flag:
        url_now =url+"?p="+str(page)
        Html = self.runUrl(url_now)
        
        if Html :
            ret = json.loads(Html)
            # print(ret)
            if ret['finished'] :
                flag = False
                # continue
            for v in ret['contents']:
                
                datas = {
                    'level':v['grade'],
                    'edu_level':v['educateGrade'],
                    'headimg':v['smallHeadImage'],
                    'specializeList':v['specializeList'],
                    'schedule':v['schedule']
                }
                where['doc_name'] = v['name']
                insertAllAndUpdate(self,datas,where,t_name,'haodf_depat_docter')
            print(page)
            page = page +1
    updateUrlListStatus(self,his_url,t_name)






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


















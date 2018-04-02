#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib
import threading
from queue import Queue
from types import MethodType
from bs4 import BeautifulSoup
import spider_tool
from spider_func import *
import json


__all__ = ['Spider']

'''
做一些初始化工作
'''
class BaseSpider(object):

    def __init__(self, LevelName=[]):
        # 业务爬取的层级名称
        # 可自己随便定义
        # 但是LevelName 定义之后必须在 spider_fun中去实现 result_user_LevelName方法
        self.LevelName = LevelName
        self.Q = {}
        
        self.B = "before_"
        self.R = "result_"
        self.F = "user_"
        
        ## 根据设置的levelName初始化对应个数的队列
        for x in LevelName:
            self.Q[x] = Queue()

    def runUrl(self, url):
        try:
            data = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as e:
            print(e.code, url)
        except urllib.error.URLError as e:
            print(e.reason, url)
        else:
            data = data.decode('UTF-8')
            return data
        return None
    ## 写队列
    def putQueue(self, url,level):

        if level in self.LevelName:
            # url = url+self.splitFlag+level
            self.Q[level].put(url)
        
        else:
            raise TypeError(
                "设置优先级队列名称中没有找到！plasee set: obj.LevelName = ['%s']" % level)
        
    ## 读取队列
    def getQueue(self,level):
        
        if not self.Q[level].empty():
            return self.Q[level].get()
        return False
    ## 根据设置的LevelName 动态添加 spider_fun.py 的方法到类中
    def createMethod(self):
        for x in self.LevelName:
            x = self.F + x
            try:
                before_x = self.B+x
                type(eval(before_x))
            except Exception as e:
                print("Notice:未找到：%s 函数" % before_x)
            else:
                self.__dict__[before_x] = MethodType(eval(before_x), self)

            # try:
            #     type(eval(x))
            # except Exception as e:
            #     raise TypeError("请定义函数：%s" % x)
            # else:
            #     self.__dict__[x] = MethodType(eval(x), self)

            try:
                result_x = self.R+x
                type(eval(result_x))
            except Exception as e:
                raise TypeError("请定义结果处理函数：%s" % result_x)
                # print("Notice:未找到：%s 函数" % result_x)
            else:
                self.__dict__[result_x] = MethodType(eval(result_x), self)

'''
    多线程类
'''
class ThreadSpider(threading.Thread):
    ### spiderObj 为一个继承自BaseSpider的对象
    def __init__(self, *, spiderObj,url=None, level=None,name=''):

        # 第一个url
        self.url = url
        self.level = level
        if isinstance(spiderObj, BaseSpider):
            self.obj = spiderObj
        else:
            raise TypeError("请传入一个继承自BaseSpider的对象")

        threading.Thread.__init__(self)
        
    ### 此处是个死循环 若爬虫有条件退出 请在此处自行修改
    # 可以改成线程多少时间没有从队列中获取到就自己死了算了
    # 或者 根据时间没有获取到 就去帮助别的队列跑 这种比较好实现
    # 不过没去写
    # 返回值默认 是 BeautifulSoup渲染的  可以通过befor方法去修改
    # 每个线程的入口
    def run(self):
        while True:
            url = self.obj.getQueue(self.level)
            if url is False:
                continue
           
            self._run(url,self.level)

        else:
            self._run(self.url,self.level)
            

    def _run(self,url,level):
        before = self.obj.B+self.obj.F+level
        result = self.obj.R+self.obj.F+level
        callback = True
        types = ''
        params = {}
        if before in dir(self.obj):
            func = "self.obj."+before
            callback,types,url,params = eval(func)(url, level,self.getName())

        if callback :
            data = self.obj.runUrl(url)

            if result in dir(self.obj):
                if data is not None:
                    func = "self.obj."+result
                    if types == 'json':
                        eval(func)(url,level, json.loads(data),self.getName(),param=params)
                    else:
                        eval(func)(url,level, BeautifulSoup(data, 'lxml'),self.getName(),param=params)

'''
    这个实现了一些爬虫的简单方法
'''
class Spider(BaseSpider):
    def __init__(self, *, firstUrl='', LevelName=['first'], ThreadNum=5,back=None):
        super().__init__(LevelName=LevelName)
        ###线程数已经没用了
        self.ThreadNum = ThreadNum
        self.firstUrl = firstUrl
        self._Headers = {
                        'Accept-Language':'zh-CN,zh;q=0.9',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        ##这里是随机取一个Agent
                        'User-Agent':spider_tool.Tool.randAgent() 
                        }
        self._Proxy = None
        ##发送的数据
        self._Data = {}
        self.back = back

    @property
    def Agent(self):
        return self._Headers['User-Agent']

    @Agent.setter
    def Agent(self, agents):
        if isinstance(agents, str):
            self._Headers['User-Agent'] = agents
        else:
            raise TypeError("agent 应该是一个字符串！")

    @property
    def Cookie(self):
        return self._Headers['Cookie']
    @Cookie.setter
    def Cookie(self,cookies):
        if isinstance(cookies, str):
            self._Headers['Cookie'] = cookies
        else:
            raise TypeError("cookie 应该是一个字符串！")

    @property
    def Referer(self):
        return self._Headers['Referer']
    @Referer.setter
    def Referer(self,ref):
        if isinstance(ref, str):
            self._Headers['Referer'] = ref
        else:
            raise TypeError("Referer 应该是一个字符串！")

    @property
    def Data(self):
        return self._Data
    @Data.setter
    def Data(self,datas):
        if isinstance(datas, dict):
            self._Data = datas
        else:
            raise TypeError("发送数据 应该是一个字典！")

    @property
    def Proxy(self):
        return self._Proxy
    @Proxy.setter
    def Proxy(self,datas):
        if isinstance(datas, dict):
            self._Proxy = datas
        else:
            raise TypeError("代理 应该是一个字典！eg:{'sock5': '127.0.0.1:1080'}")

    ##获取网页内容的方法
    #这个装饰器是处理网页异常的，可以实现异常记日志或者异常重新插入队列
    
    # @spider_tool.Tool.myExcept('url')
    def runUrl(self,url,method='Post'):


        if url.find('http') == -1 :
            url = "https:"+url

        if self._Proxy is not None:
            proxy_support = urllib.request.ProxyHandler()
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
        
        data = urllib.parse.urlencode(self._Data).encode(encoding='UTF8')
        req = urllib.request.Request(url, data, self._Headers)    
        html = urllib.request.urlopen(req).read()
        # charset= chardet.detect(html)
        return html
        # return html.decode(charset['encoding'],"ignore").encode('utf-8',"ignore")
    ####
    #这个是开始的方法
    def start(self):
        ###动态添加方法到类中
        super().createMethod()
        #第一个url 加入队列
        if self.firstUrl :
            self.Q[self.LevelName[0]].put(self.firstUrl,self.LevelName[0])
        

        ## 这个实现的是根据levelName 去开启线程
        #第一级 开一个线程跑
        #第二级 开两个
        #类推
        #可自行修改
        myThread = []
        for k,x in enumerate(self.LevelName):
            for x2 in range(0,k+1):
                myThread.append(ThreadSpider(spiderObj=self,level=x))
        # myThread = [(ThreadSpider(spiderObj=self,level=x) for k2 in range(0,k+1)) for k,x in enumerate(self.LevelName)]
        for x in myThread:
            x.start()
        for x in myThread:
            x.join()
    
    ####
    #这个是因为我将所要url记到mysql了 如果中途跑死了 可以自行从这里恢复
    def getUrlStatus(self):
    
        m = mysql.MyMysql('Local')
        m.conn()
        sql = "select url,level from spider_url_list where level='three' group by url"
        ret = m.fetchall(sql,())

        for x in ret:
            self.putQueue(x['url'],x['level'])


if __name__ == '__main__':
    
    def result_user_first(self,url,level,soup):
        # print(soup.title)
        lilist = soup.findAll('li')
        # print(lilist)
        for x in lilist:
            print(x.a['href'],x.a.string)

    firstUrl = "https://m.haodf.com/touch/province/list.htm"
    LevelName = ['first']
    s = Spider(firstUrl=firstUrl, LevelName=LevelName)
    s.createMethod()
    data = s.runUrl(firstUrl)
    # print(data)
    soup = BeautifulSoup(data,'lxml')
    # print(soup)
    s.result_user_first(firstUrl,'first',soup)

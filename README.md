# Spider
一个自己写的python3的简单到发指的爬虫
----

本实例是测试所写，所产生的法律问题请自行负责
-----

#依赖
BeautifulSoup 安装：pip3 install beautifulsoup4

#LevelName
一个列表 eg:
```python
LevelName = ['first','second','three','four','five']
```
    后面自定义结果处理方法命名方式为：
    before_user_ + levelName  && result_user_ + levelName
    before方法为自选 请求url之前调用这个方法
    result为必须去实现的方法 请求url之后将url返回的结果传入这个方法

#使用
```python
import spider_class

LevelName = ['first','second']
firstUrl = "https://m.haodf.com/touch/province/list.htm"

s = spider_class.Spider(firstUrl=firstUrl, LevelName=LevelName)
# s = spider_class.Spider(back=True, LevelName=LevelName)
s.start()
```
spider_fun.py中:
```python
###请求完url之后 调用的方法
def result_user_first(self,url,level,soup,t_name,*,param={}):
  pass
  #self为Spider类的实例
  #url为请求的地址
  #soup为网页结果的beautifulsoup对象
  #t_name 为线程名称
def result_user_second(self,url,level,soup,t_name,*,param={}):
  pass
###不是必须的
###before是表示在请求url之前调用这个方法
def before_user_first(self,url,level,t_name,*,param={}):
  #第一个参数表示是否去请求这个url
  #第二个是解析网页类容方式 默认是beautifulsoup 
  #url 是请求的url
  #后面为传参
  return True,'json',url,{'hospital_name':hospital_name}
```

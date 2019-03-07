#!/usr/bin/env python
# -*-encoding:UTF-8-*-

# 传统的数据库访问MySQL等 非常直白
# 1、直接将sql语句硬编码嵌入到代码中，可以通过将这些数据保存到文件中进行解决
# 2、存在大量的重复的代码。可以通过编写额外的代码尽可能解决代码重复的问题
# 3、如果使用Python模块访问数据库，就会将整个项目栓死在某个数据库上
#

from pymysql import *
import json
from django.http import HttpResponse

def processDB(request):
    # 链接数据库
    db = connect('localhost','root','123','testdb',charset = 'utf8')
    cursor = db.cursor()
    sql = 'select * from EMPLOYEE'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    fields = ['First_Name','Last_Name','Age','Sex','Income']
    records = []
    for row in results:
        # 使用Python的专有函数讲数据读取出来
        records.append(dict(zip(fields,row)))
    return  HttpResponse(json.dumps(records))




'''
MTV 模式（Model Template View）

MVC（Model View Controller）是一种Web架构模式，将业务逻辑。模型数据库和用户分开

MVC模式的三要素
1、Model（数据库模型）。
2、Views（视图）
3、Controller（控制器）。

MTV（Model Template View）
1、Model（数据模型，通过Model的ORM访问数据库）。
2、Template（view将数据灌输到Template模板返回给用户）。
3、View（视图）映射函数，承上启下返回Template，向下访问模板。
'''

#ORM方式操作
# 表示一个表的话，就是对象的集合，数据库表的每一行就是一个对象

# ORM（对象关系的映射）
# mysql-client（只管MySQL）
'''
1、安装sudo apt-get install mysql-client
2、python manage.py startapp testdb
3、在setting.py里面的INSTALLED_APPS 添加‘testdb’
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testdb',
]
4、在setting.py中甚至MySQL数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdb',
        'PASSWORD':'123',
        'HOST':'127.0.0.1'
    }
}
5、建立模型
在model.py里面编写模型类
class Movie(models.Model):
    name = models.CharField(max_length=50)
    show_time = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    
6、python manage.py makemigrations testdb   
7、python manage.py migrate 创建表格

成功之后在控制台里面可以记性操作插入和查询如下：
插入：
from testdb.models import Movie
m1 = Movie(name = "疯狂外星人",show_time='2019-1-1',type='喜剧')
m1.save()
查询：
a = Movie.objects.all()
for x in a:
    print(x.name)
    
疯狂外星人

'''
from testdb.models import Movie

def testORM(request):
    result = Movie.objects.all()
    name = ''
    for x in result:
        name = x.name
        #break;
    return HttpResponse(name)

# 对数据表的insert、update和delete
def changeData(request):
    #向teatDB中插入3条数据

    m1 = Movie(name = "狂暴巨兽",show_time='2018-1-1',type='惊险，科幻')
    m1.save()
    m2 = Movie(name="复仇者联盟3", show_time='2018-5-11', type='科幻、动作')
    m2.save()
    m3 = Movie(name="泰囧", show_time='2016-1-1', type='喜剧、动作')
    m3.save()

    '''
    # 查询数据出来之后再修改
    m4 = Movie.objects.get(name = "狂暴巨兽")
    m4.name = '太空堡垒'
    m4.save()
    '''
    # 删除单条数据
    '''
    m5 = Movie.objects.get(name="泰囧")
    m5.delete()
    '''
    # 删除全部数据
    # Movie.objects.all().delete()
    return  HttpResponse("数据修改成功！！")

# 数据过滤
def filter(request):
    # 过滤所有的数据
    all = Movie.objects.all()
    result = ''
    for d in all:
        result = result + d.name + ','

    # 按照具体值查询
    # dataSet = Movie.objects.filter(name = '狂暴巨兽') # 将名字为狂暴巨兽的电影查询出来而不是过滤掉
    dataSet = Movie.objects.filter(show_time='2016-1-1',type='喜剧、动作')
    result = ''
    for d in dataSet:
         result = result + d.name + ','

    # where name like '%abc' 模糊查询
    dataSet = Movie.objects.filter(name__contains='3')
    result = ''
    for d in dataSet:
         result = result + d.name + ','
    return HttpResponse(result)


# 获得单个对象
def oneObject(request):
    # filter return QuerySet
    # get 返回一个对象（模型对象）
    # 利用print打印查看不同的两个对象
    #<class 'testdb.models.Movie'>
    #<class 'django.db.models.query.QuerySet'>
    try:
        m = Movie.objects.get(name = '流浪地球')
        print(type(m))                                          # 返回的是一个Movie
        print(type(Movie.objects.filter(name = '流浪地球')))     # 返回的是一个QuerySet
    except Movie.DoesNotExist:
        return HttpResponse('没有查询到任何数据！')
    except Movie.MultipleObjectsReturned:
        return HttpResponse('查询结果多于一条记录')
    # 如果没有查到任何数据或者多于一条数据时候，会抛出DoesNotExist异常或MultipleObjectsReturned异常
    #出现异常的情况使用try 和 except 将异常包含起来，以免会出现报错等意外情况
    return  HttpResponse("正常查询成功！")

# 数据排序 name:正常的排序，-name：逆序 ,也可以对多个属性值进行排序 默认升序列，加‘-’表示逆序
def dataOrder(request):
    dataSet = Movie.objects.order_by('-name','type')
    result = ''
    for d in dataSet:
        result = result + d.name + ','
    return HttpResponse(result)

# 连锁查询
def multQuery(request):
    dataSet = Movie.objects.filter(type__contains='科幻').order_by('name')
    result = ''
    for d in dataSet:
        result = result + d.name + ','
    return HttpResponse(result)

# 限制返回的数据(返回查询结果的子集)
'''
select * from table1 where name like '%abc' limit 1,10  返回从第二条数据开始的10条数据
'''
def limitData(request):
    # QuerySet 不支持负数 如果使用负数就会抛出异常，如：[1:-3]
    '''
    AssertionError at /limitData

    Negative indexing is not supported.
    '''
    # dataSet = Movie.objects.order_by('name') # 返回所有的数据
    dataSet = Movie.objects.order_by('name')[1:3] # limit 1,2
    result = ''
    for d in dataSet:
        result = result + d.name + ','
    return HttpResponse(result)

# 更新指定列
'''
    m = Movie.objects.get(name = '狂暴巨兽')
    m.name = '太空堡垒'
    m.save()     # 更新所有的而数据，有点不好就是，可能其他的进程正在
    使用数据库的某一列数据，这样就会导致数据冲突
    所以就需要使用update来进行数据的更新
    update testdb_movie set name = '太空堡垒',type = '科幻、冒险',show_time = '2018-4' where name = '狂暴巨兽' 
'''
def updateData(request):
    # update testdb_movie set name = '蜘蛛侠2' where name = ’狂暴巨兽‘
    Movie.objects.filter(name = '狂暴巨兽').update(name = '蜘蛛侠2');
    return  HttpResponse("更新成功！")
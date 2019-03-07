#!/usr/bin/env python
# -*-encoding:UTF-8-*-

'''
from django import template
t = template.Template('My name is {{name}}.')
c = template.Context({'name':'Bill'})
t.render(c)
u'My name is Bill.'

'''
from django.http import HttpResponse
from django import template

def simpleTemplate(request):
    t = template.Template('My name is {{name}}.')
    c = template.Context({'name': 'Bill'})
    return HttpResponse(t.render(c))

# 同一个模板，多个上下文（Context）
'''
比较糟糕的写法，应该讲创建的Template对象的工作放到for循环外面
for name in ('John','Mike','Mary'):
    t = Template('Hello,{{name}}')
    t.render(Context({'name':name}))
  
比较好的写法
t = Template('Hello,{{name}}')
for name in ('John','Mike','Mary'):
    print(t.render(Context({'name':name})))
    
Hello,John
Hello,Mike
Hello,Mary
'''

def multContext(request):
    html = '<ul>'
    t = template.Template('<li>Today is {{day}}</li>')
    for day in ('Monday','Tuesday','Wednessday'):
        c = t.render(template.Context({'day':day}))
        html += c
    html += '</ul>'
    return HttpResponse(html)

# 向上下文传递字典和列表
'''
字典
person = {'name':'Mary','age':40}
t = Template('{{person.name}} is {{person.age}} years old.')
c = Context({'person':person})
t.render(c)
u'Mary is 40 years old.'
列表
person1 = ['Mike',38]
t = Template('{{person.0}} is {{person.1}} years old.')
c = Context({'person':person1})
t.render(c)
u'Mike is 38 years old.'
'''

'''
# 向上下文传递对象

查找顺序
{{person.name}}

1.person['name']
2.person.name  属性名优秀于方法，如果属性和方法同名的话，是会优先访问属性
3.person.name()
4.person[name]
'''

# 如何处理无效变量
# 变量在模板中存在，但是并没有通过Context指定
# 变量区分大小写
'''
from django.template import Template,Context
t = Template("Your name is {{name}}.")
t.render(Context())
u'Your name is .'
t.render(Context({'var':'hello'}))
u'Your name is .'
t.render(Context({'name':'abc'}))
u'Your name is abc.'
t.render(Context({'aName':'abc'}))
u'Your name is .'
t.render(Context({'Name':'abc'}))
u'Your name is .'
t.render(Context({'NAME':'abc'}))
u'Your name is .'
'''


# 按照字典的方式向Context添加或者删除对象

'''
t = Template('This is a {{field}}. That is a {{field2}}')
c = Context({'field1':'Banana','field2':'car'})
t.render(c)
u'This is a . That is a car'
t = Template('This is a {{field1}}. That is a {{field2}}')
c = Context({'field1':'Banana','field2':'car'})
t.render(c)
u'This is a Banana. That is a car'
c['field1']
'Banana'
c['field2']
'car'
del c['field1']  # 删除field1 之后会报错
c['field1']
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/home/toohoo/PycharmProjects/SecondDjango/venv/local/lib/python2.7/site-packages/django/template/context.py", line 87, in __getitem__
    raise KeyError(key)
KeyError: 'field1'
c.get('field1')
t.render(c)
u'This is a . That is a car'   # 前面的是串
c['field1'] = 'abcd'     # 添加新的值，然后再输出
t.render(c)
u'This is a abcd. That is a car'
'''

# 从磁盘装载模板文件 之前的模板都是固化，硬编码的形式，下面使用从磁盘中读取模板方法
# 修改默认模板文件目录
from django.template.loader import  get_template
import datetime

def loadTemplateFile(request):
    now = datetime.datetime.now()
    t = get_template('t.html')
    html = t.render({'current_date':now})
    return HttpResponse(html)

# 更简单的装载方法：使用函数render_to_response
from django.shortcuts import render_to_response
def loadTemplateFile1(request):
    now = datetime.datetime.now()
    return render_to_response('t.html',{'current_date':now})

# 字段比较多的情况
def loadTemplateFile2(request):
    current_date = datetime.datetime.now()
    field1 = 'hello'
    field2 = 'world'
    field3 = 'abc'
    #return render_to_response('t.html',{'current_date':current_date,'field1':field1,'field2':field2,'field3':field3})
    # locals()要求字段名和模板中的字段名相同
    return render_to_response('t.html',locals())

# 修改默认的模板目录
def loadTemplateFile3(request):
    current_date = datetime.datetime.now()
    field1 = 'hello'
    field2 = 'world'
    field3 = 'abc'
    # return render_to_response('x.html',{'current_date':current_date,'field1':field1,'field2':field2,'field3':field3})
    return render_to_response('x.html', locals())


#if-else标签的简单应用
def ifelseTemplate(request):
    current_date = datetime.datetime.now()
    field1 = 'hello'
    field2 = 'world'
    field3 = 'abc'
    today_is_weekend = 0
    # return render_to_response('x.html',{'current_date':current_date,'field1':field1,'field2':field2,'field3':field3})
    return render_to_response('t.html', locals())

'''
if-else的真假判断
1.空列表（[]）
2.空元组（（））
3.空字典（{}）
4、空字符串（''）
5、零值
6、None
7、False

'''

# if-else 标签的多值条件与嵌套
# and or not
def multCondition(request):
    current_date = datetime.datetime.now()
    field1 = 'hello'
    field2 = 'world'
    field3 = 'abc'
    today_is_weekend = 0
    return render_to_response('t.html', locals())

# for标签
'''
for X in Y:

{% for%}

{% endfor %}

for标签不支持break和continue

内置变量forloop.counter{从1开始}，forloop.counter0 (从0开始)
forloop.revcounter 和forloop.revcounter0
表示循环中剩余项的值

forloop.first(第一次执行for为true)和forloop.last(最后一次执行for，为true)
'''
def forlist(request):
    persons = [{'name':'Bill','age':30},{'name':'Mike','age':40},{'name':'Mary','age':50}]
    return render_to_response('for.html',locals())

# ifequal和ifnotequal(equal模板)
# 这两个标签只能使用字符串、整数和浮点数，不能使用字典、列表和布尔
def equalVar(request):
    user = 'geek'
    currentUser = 'geekori'
    return render_to_response('equal.html',locals())

# 单行注释和多行注释
'''
    {# 1、 This is comment 单行注释，跨行是会失败的,例如下面的代码 #}
    {#  abc
        xyz
    #}
    {%  comment  这种注释是不会发送到客户端的，但是很多时候，我们并不希望将注释发送过去%}
        多行注释
    {% endcomment %}
    <!--Html的注释是会发送到客户端的--> 
    所以我们使用Django模板的注释
'''

# 过滤器
'''
过滤器：对模板变量的二次加工
1、lower：将模板变量的值都变成小写
2、upper：将模板的值都变成大写
3、trucatewords：截取前n个单词
4、addslashes：在任何的反斜杠、单引号或者双引号前面添加反斜杠
5、date：指定的格式化字符串参数格式化date或者datetme对象
6、length：用于返回模板变量的长度
'''
def filter(request):
    mytime = datetime.datetime.now()
    name = "Bill"
    productName = 'iPhone Android 黑莓 宝马'
    return render_to_response('filter.html',locals())


# 引用模板（include标签）
def include(request):
    main1 = "hello world"
    main2 = "I love you"
    main3 = "It's hot"
    t1 = "这是第一个子模板"
    t2 = "这是第二个子模板"
    t3 = "这是第三个子模板"
    return render_to_response('main.html', locals())

# 模板继承
'''
比include的使用更加优雅

'''

def sub1(request):
    car_product = "特斯拉"
    return render_to_response('sub1.html', locals())

def sub2(request):
    mobile_product1 = "iPhone"
    mobile_product2 = "黑莓"
    return render_to_response('sub2.html', locals())


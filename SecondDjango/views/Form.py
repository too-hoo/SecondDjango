#!/usr/bin/env python
# -*-encoding:UTF-8-*-

# 表单
# 获取客户端请求的信息
from django.http import HttpResponse
from django.shortcuts import render_to_response

def requestInfo(request):
    result = 'path:%s' % request.path
    result = result + '<br>host:%s' %request.get_host()
    result = result + '<br>full_path:%s' %request.get_full_path()
    result = result + '<br>port:%s' %request.get_port()
    result = result + '<br>https:%s'%request.is_secure()
    # request.META:Python字典属性，包含所有的Http请求头,如果没有请求头HTTP_Accept时候，会抛出异常
    try:
        result = result + '<br>Accept:%s' %request.META['HTTP_ACCEPT']
    except KeyError:
        result = result + '<br>HTTP请求头获取异常'
    except UnicodeDecodeError:
        result = result + '<br>HTTP请求头获取异常'
    except KeyError:
        result = result + '<br>HTTP请求头获取异常'
    '''
    values = request.META.items()
    sorted(values)
    html = []
    for key,value in values:
        html.append('<tr><td>%s<td><td>%s<td></tr>' %(key,value))
    return HttpResponse('<table>%s<table>'%'\n'.join(html))
    '''
    return HttpResponse(result)

# 处理表单（Form）提交数据
def search_form(request):
    return render_to_response('search_form.html')


from testdb.models import Movie
def search(request):
    # 这里涉及到一个字典存储的问题，如果是get请求的话就映射到get字典里面
    # 如果是post的话就是映射到post请求里面
    # 这里的name对应search_form.html表单里面的name
    if 'name' in request.GET:
        message = 'You searched for :%s' %request.GET['name']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

# 从数据库中查询数据
def search2(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    if 'name' in request.GET:
        name = request.GET['name']
        movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
        return render_to_response('search_result.html',{'movies':movies,'query':name})
    else:
        return HttpResponse('Please submit a search term.')

# 改进表单
# 出错要点击回退
def search3(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    if 'name' in request.GET:
        name = request.GET['name']
        movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
        return render_to_response('search_form_ext.html',{'movies':movies,'query':name})
    else:
        return render_to_response('search_form_ext.html',{'error':True})

# 表单的简单校验
# 改进表单
def searchVerify(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    error = False
    if 'name' in request.GET:
        name = request.GET['name']
        # name 必须要有值
        # print(type(name))
        if not name:
            error = True
        elif len(name) > 10:
            error = True
        else:
            movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
            return render_to_response('search_form_ext1.html',{'movies':movies,'query':name})
    # 注意这里使用flag的形式传值控制
    return render_to_response('search_form_ext1.html',{'error':error})

def searchVerify1(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    errors = []      # 使用列表进行不同信息的接收
    print(errors)
    if 'name' in request.GET:
        name = request.GET['name']
        # name 必须要有值
        print(name)
        if not name:
            errors.append("请输入电影的类型名！")
        elif len(name) > 10:
            errors.append("电影类型名长度不能大于10")
        else:
            movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
            return render_to_response('search_form_ext2.html',{'movies':movies,'query':name})
    # 注意这里使用flag的形式传值控制
    return render_to_response('search_form_ext2.html',{'errors':errors})

# 复杂的表单校验
def searchVerify2(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    errors = []      # 使用列表进行不同信息的接收
    if 'name' in request.GET:
        name = request.GET['name']
        value1 = request.GET['value1']
        value2 = request.GET['value2']
        # name 必须要有值
        if not name:
            errors.append("请输入电影的类型名！")
        if not value1:
            errors.append("必须提供value1！")
        if not value2:
            errors.append("必须提供value2！")
        if not errors:
            movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
            return render_to_response('search_form_ext3.html',{'movies':movies,'query':name})
    # 注意这里使用flag的形式传值控制
    return render_to_response('search_form_ext3.html',{'errors':errors})

# 编写Form类
# django.forms.Form

# 在视图中使用Form对象
from testdb.forms import MyForm
# 默认开启了防止跨域网站的模拟用户的身份进行攻击，为了能使得表单返回正确的内容，将这个开启关闭
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt        # 这个需要手动输入，不会自动生成
def contact(request):
    if request.method =='POST':    # post方法请求
        form = MyForm(request.POST)
        if form.is_valid():
            print("完成与业务相关的工作")
            return HttpResponse("OK")
        else:
            return render_to_response('my_form.html',{'form':form})     # 返回到表单，如果出现错误就会在文本框的上面显示错误
    else:
        #form = MyForm(initial={'name':'tuhua','email':'hello@toohoo.com','message':'没有信息'}) # 设置默认的表单信息
        form = MyForm()
        return render_to_response('my_form.html',{'form':form})     #否则就是get方法请求了

# 改变字段的显示风格

# 限制输入框的输入最小值和最大值

# 设置表单的默认初始值

# 自定义检验规则

# 指定标签：使用label关键字将原来的表单字段名称覆盖

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
def search1(request):
    # 这里涉及到一个字典存储的问题，如果是get请求的话就映射到get字典里面
    # 如果是post的话就是映射到post请求里面
    # 这里的name对应search_form.html表单里面的name
    if 'name' in request.GET:
        message = 'You searched for :%s' %request.GET['name']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

# 从数据库中查询数据
def search1(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    if 'name' in request.GET:
        name = request.GET['name']
        movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
        return render_to_response('search_result.html',{'movies':movies,'query':name})
    else:
        return HttpResponse('Please submit a search term.')

# 改进表单
# 出错要点击回退
def search(request):
    # 使用filter之后完全不用sql语句的，简直刷新我的观念啊！
    if 'name' in request.GET:
        name = request.GET['name']
        movies = Movie.objects.filter(type__icontains=name)     # 按类型查找
        return render_to_response('search_form_ext.html',{'movies':movies,'query':name})
    else:
        return render_to_response('search_form_ext.html',{'error':True})

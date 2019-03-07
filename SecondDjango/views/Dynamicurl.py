#!/usr/bin/env python
# -*-encoding:UTF-8-*-
from django.http import HttpResponse
from django.http import Http404,HttpResponse

def fun1(request):
    return HttpResponse('fun1')

def fun2(request):
    return HttpResponse('fun2')

def fun3(request):
    return HttpResponse('fun3')

def fun(request,value):
    try:
        value = int(value)
    except ValueError:
        # 需要导入一个包
        raise Http404()
    result = 'fun%s' % value
    return HttpResponse(result)
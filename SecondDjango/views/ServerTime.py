#!/usr/bin/env python
# -*-encoding:UTF-8-*-
from django.http import HttpResponse
import datetime

# 松耦合的原则：是一个重要的保证互换性的软件开发方法，这个文件本身不知道自己会被映射到哪里，可以是深层路径也可以是根路径
# 例如URL.py文件里面所记录的那样
def currentDateTime(Request):
    now = datetime.datetime.now()
    html = "<html><body>当前时间是： %s.</body></html>" % now
    return HttpResponse(html)
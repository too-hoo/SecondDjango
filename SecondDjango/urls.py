#!/usr/bin/env python
# -*-encoding:UTF-8-*-

"""SecondDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from .views import First
from .views import ServerTime
from .views import Dynamicurl
from .views import MyTemplate
from .views import DB
from .views import Form
from .views import CommentViewClass

from django.views.generic.base import RedirectView

# 动态URL的使用
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hh/',First.index),
    url(r'^time/$',ServerTime.currentDateTime),
    url(r'^$',ServerTime.currentDateTime),
    url(r'^time1$',ServerTime.currentDateTime),
    #url(r'^fun/1$',Dynamicurl.fun1),
    #url(r'^fun/2$',Dynamicurl.fun2),
    #url(r'^fun/3$',Dynamicurl.fun3),
    # 映射变成正则表达式
    url(r'^fun/(\d{1,3})/$',Dynamicurl.fun),
    url(r'^simpleTemplate/$',MyTemplate.simpleTemplate),
    url(r'^multContext/$',MyTemplate.multContext),
    url(r'^loadTemplateFile/$',MyTemplate.loadTemplateFile),
    url(r'^loadTemplateFile1/$',MyTemplate.loadTemplateFile1),
    url(r'^loadTemplateFile2/$',MyTemplate.loadTemplateFile2),
    url(r'^loadTemplateFile3/$',MyTemplate.loadTemplateFile3),
    url(r'^ifelseTemplate/$',MyTemplate.ifelseTemplate),
    url(r'^multCondition/$', MyTemplate.multCondition),
    url(r'^forlist/$', MyTemplate.forlist),
    url(r'^equalVar/$', MyTemplate.equalVar),
    url(r'^filter/$', MyTemplate.filter),
    url(r'^include/$', MyTemplate.include),
    url(r'^sub1/$', MyTemplate.sub1),
    url(r'^sub2/$', MyTemplate.sub2),
    url(r'^processDB/$', DB.processDB),
    url(r'^testORM/$', DB.testORM),
    url(r'^changeData/$', DB.changeData),
    url(r'^dataFilter/$', DB.filter),
    url(r'^oneObject/$', DB.oneObject),
    url(r'^dataOrder/$', DB.dataOrder),
    url(r'^multQuery/$', DB.multQuery),
    url(r'^limitData/$', DB.limitData),
    url(r'^updateData/$', DB.updateData),
    url(r'^requestInfo/$', Form.requestInfo),
    url(r'^searchForm/$', Form.search_form),
    url(r'^search/$', Form.search),
    url(r'^searchVerify/$', Form.searchVerify),
    url(r'^searchVerify2/$', Form.searchVerify2),
    url(r'^contact/$', Form.contact),
    url(r'^myview/$', CommentViewClass.MyView.as_view()),   # 使用里面内置的方法返回相应的程序，注意是as_view()
    url(r'^homepage/$',CommentViewClass.HomePageView.as_view()),
    url(r'^geekori/$', RedirectView.as_view(url='https://geekori.com')),
    url(r'^baidu/$', RedirectView.as_view(url='https://baidu.com')),
    url(r'^movie_view/$',CommentViewClass.MovieView.as_view()),
    url(r'^query_movie_view/$',CommentViewClass.QueryMovieView.as_view()),
    url(r'^param_query_movie_view/$', CommentViewClass.ParamQueryMovieView.as_view()),
    # <pk>表示主键 \d+ 表示至少有一个数字
    url(r'^movie_detail/(?P<pk>\d+)/$', CommentViewClass.MovieDetailView.as_view()),
]

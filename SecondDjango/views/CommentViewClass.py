#!/usr/bin/env python
# -*-encoding:UTF-8-*-

# 通用视图类

# 简单的通用视图类
from django.http import HttpResponse
from django.views.generic import View

class MyView(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse('Hello World!')

# 可以向模板中传递变量值的通用类
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = "product1.html"
    def get_context_data(self, **kwargs):
        context = super(HomePageView,self).get_context_data(**kwargs)
        context['phone_product1'] = 'iPhone'
        context['phone_product2'] = 'Android Mobile'
        return context

# 用来跳转的通用视图类

# 列表视图(listView) 需要listview，需要Movie
from django.views.generic import ListView,DeleteView
from testdb.models import Movie

# 妈的！！要区分context_object_name 和 comtext_object_name啊啊！！ 后面没有智能提示的！！！
class MovieView(ListView):
    model = Movie
    template_name = 'movie_view.html'
    context_object_name = 'movies'

class QueryMovieView(ListView):
    model = Movie
    template_name = 'movie_view.html'
    context_object_name = 'movies'
    def get_queryset(self):
        return super(QueryMovieView,self).get_queryset().filter(type='喜剧')

# 通过地址设置参数：http://127.0.0.1:8000/param_query_movie_view/?name=流浪地球
class ParamQueryMovieView(ListView):
    model = Movie
    template_name = 'movie_view.html'
    context_object_name = 'movies'
    def get_queryset(self):
        name = self.request.GET.get('name')
        return super(ParamQueryMovieView,self).get_queryset().filter(name=name)

# 细节视图(DetailVIew)
# 浏览器的访问路径为这样：http://127.0.0.1:8000/movie_detail/13/
class MovieDetailView(DeleteView):
    queryset = Movie.objects.all()
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
    def get_object(self, queryset=None):
        obj = super(MovieDetailView,self).get_object(queryset=queryset)
        return obj


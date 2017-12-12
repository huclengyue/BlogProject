#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blog import views

app_name = 'blog'
urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.index, name="index"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name="archives"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name="category"),

]

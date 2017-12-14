#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blog import views

app_name = 'blog'
urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="detail"),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchiveView.as_view(), name="archives"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name="category"),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name="tag"),
    url(r'^search/$', views.search, name="search"),

]

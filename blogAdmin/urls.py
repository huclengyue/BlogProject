#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blogAdmin import views

app_name = 'blogAdmin'
urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.admin_index, name="index"),
    # url(r'^$', views.admin_login, name="login"),
    url(r'^login/$', views.admin_login, name="login"),
    # url(r'^search/$', views.search, name="search"),

]

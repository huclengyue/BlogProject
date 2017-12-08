#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blog import views

urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.index, name="index")
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blogAdmin import views, article

app_name = 'blogAdmin'
urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.admin_index, name="index"),
    # url(r'^$', views.admin_login, name="login"),
    url(r'^login/$', views.admin_login, name="login"),
    url(r'^article/$', views.AdminPost.as_view(), name="article_list"),
    url(r'^article/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="article_edit"),
    url(r'^article/delete/(?P<pk>[0-9]+)/$', views.admin_delete, name="article_delete"),
    # 文章
    # 发布文章
    url(r'^article/publish/$', article.article_publish, name="article_publish"),
    # 发布文章按钮
    url(r'^article/create/$', article.article_create, name="article_create"),
    # 修改文章
    url(r'^article/modify/$', article.article_create, name="article_modify"),
    # 链接
    url(r'^links/$', views.admin_links, name="admin_links"),
    url(r'^links/save/$', views.admin_links_save, name="admin_links_save"),
    url(r'^links/delete/$', views.admin_links_delete, name="admin_links_delete"),

    # 系统设置
    url(r'^setting/$', views.admin_setting, name="admin_setting"),

    # url(r'^search/$', views.search, name="search"),

]

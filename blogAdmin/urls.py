#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from blogAdmin import views, article, profile, other

app_name = 'blogAdmin'
urlpatterns = [
    # 函数（第一个参数是网址，第二个参数是处理函数）
    url(r'^$', views.admin_index, name="index"),
    # url(r'^$', views.admin_login, name="login"),
    url(r'^login/$', views.admin_login, name="login"),

    # 文章
    url(r'^article/$', article.AdminPost.as_view(), name="article_list"),
    url(r'^article/(?P<pk>[0-9]+)/$', article.PostDetailView.as_view(), name="article_edit"),
    url(r'^article/delete/(?P<pk>[0-9]+)/$', article.admin_delete, name="article_delete"),
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
    # 个人设置
    url(r'^profile/$', profile.admin_profile, name="admin_profile"),
    url(r'^password/$', profile.admin_password, name="admin_password"),
    # 其他管理
    url(r'^comments/$', other.AdminComment.as_view(), name="admin_comments"),
    url(r'^category/$', other.admin_category, name="admin_category"),
    url(r'^category/delete/$', other.admin_category_delete, name="admin_category_delete"),
    url(r'^tag/delete/$', other.admin_tag_delete, name="admin_tag_delete"),
    url(r'^category/save/$', other.admin_category_save, name="admin_category_save"),

    # 附件管理
    url(r'^attach/$', views.attach, name="admin_attach"),

    # url(r'^search/$', views.search, name="search"),

]

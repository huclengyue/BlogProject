#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import hashlib
from urllib import parse

from django import template
from django.db.models.aggregates import Count

from blog.models import Friendly, Category, Tag
from blogAdmin.models import User
from comments.models import Comment

register = template.Library()


@register.simple_tag()
def get_friendly_link_count():
    return Friendly.objects.all().count()


# 分类
@register.simple_tag()
def get_all_category():
    return Category.objects.all()


# 当前是否激活
@register.simple_tag()
def get_is_active(url, active):
    if url == active:
        return 'active'
    else:
        return 'normal'


# 当前是否激活
@register.simple_tag()
def get_is_active_sub(url):
    if url == '/xadmin/comments/' or url == '/xadmin/category/':
        return 'active subdrop'
    else:
        return ''


# 用户信息
@register.simple_tag()
def get_user_info():
    return User.objects.first()


@register.simple_tag()
def get__all_categories():
    # 记得在顶部引入 count 函数
    return Category.objects.annotate(num_posts=Count('post')).order_by('name')


@register.simple_tag()
def get_all_tags():
    return Tag.objects.annotate(num_posts=Count('post')).order_by('name')


@register.simple_tag()
def get_random_color():
    color_list = ['purple ', 'inverse', 'danger', 'success', 'info', 'primary', 'warning',
                  'default', ]
    return color_list[random.randint(0, len(color_list) - 1)]


# 评论列表
@register.simple_tag()
def get_recent_comment():
    return Comment.objects.all().order_by('-created_time')


# 评论列表
@register.simple_tag()
def get_file_name(file_path):
    return file_path.split("/")[-1][:15]


@register.simple_tag()
def gravatar_url(email, size=40):
    default = "https://example.com/static/images/defaultavatar.jpg"
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email.lower().encode("utf8")).hexdigest(), parse.urlencode({'d': default, 's': str(size)}))

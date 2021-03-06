#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from urllib import parse

from django import template
from django.db.models.aggregates import Count

from blog.models import Post, Category, Tag, BlogSet, Friendly, Catalog
from blogAdmin.models import Attach, User
from comments.models import Comment

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


@register.simple_tag()
def get_recent_comment(num=5):
    return Comment.objects.all().order_by('-created_time')[:num]


@register.simple_tag()
def archives():
    return Post.objects.dates("created_time", 'year', order="DESC")


@register.simple_tag()
def get_up_article(key):
    try:
        return Post.objects.filter(id__gt=key).order_by('id')[0]
    except:
        return None


@register.simple_tag()
def get_down_article(key):
    try:
        return Post.objects.filter(id__lt=key)[0]
    except:
        return None


# 分类模板
@register.simple_tag()
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)  # 分类模板


@register.simple_tag()
def get_tags():
    # 查找所有TAG  并且 将tag的文章数保存到num_posts中 并且过滤num_posts==0的tag
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0).order_by(
        'num_posts', order="DESC")


@register.simple_tag()
def get_blog_set():
    return BlogSet.objects.first()


@register.simple_tag()
def get_friendly_link():
    return Friendly.objects.all()


@register.simple_tag()
def get_catalog():
    return Catalog.objects.all()


@register.simple_tag()
def get_post_count():
    return Post.objects.count()


@register.simple_tag()
def get_attach_count():
    return Attach.objects.count()


@register.simple_tag()
def get_tags_count():
    return Tag.objects.count()


@register.simple_tag()
def get_author():
    user = User.objects.first()
    if user.nickname:
        return user.nickname
    else:
        return user.username


@register.simple_tag()
def avatar_url():
    user = User.objects.first()
    if user.avatar:
        return user.avatar
    else:
        default = "https://example.com/static/images/defaultavatar.jpg"
        return "https://www.gravatar.com/avatar/%s?%s" % (
            hashlib.md5(user.email.lower().encode("utf8")).hexdigest(),
            parse.urlencode({'d': default, 's': str(60)}))


# 当前是否激活
@register.simple_tag()
def is_active(url, active):
    if url == active:
        return 'menu-item-active'
    else:
        return ''

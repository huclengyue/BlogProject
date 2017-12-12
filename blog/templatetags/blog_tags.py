#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

from blog.models import Post, Category

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag()
def archives():
    return Post.objects.dates("created_time", 'month', order="DESC")


# 分类模板
@register.simple_tag()
def get_categories():
    return Category.objects.all()

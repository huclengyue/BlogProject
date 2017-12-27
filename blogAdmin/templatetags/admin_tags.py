#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

from blog.models import Friendly, Category

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

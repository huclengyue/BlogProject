#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

from blog.models import Friendly

register = template.Library()


@register.simple_tag()
def get_friendly_link_count():
    return Friendly.objects.all().count()

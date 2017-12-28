#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from BlogProject import settings
from blog.models import Category, Tag
from blogAdmin import utils
from comments.models import Comment


@login_required
def admin_comments(request):
    if request.method == 'GET':
        return render(request, 'admin/comment_list.html')


@login_required
def admin_category(request):
    if request.method == 'GET':
        return render(request, 'admin/category.html')


@login_required
def admin_category_delete(request):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=request.POST['mid'])
        if category is None:
            return HttpResponse(utils.get_failure_with_msg("分类不存在"), content_type="application/json")
        else:
            category.delete()
            return HttpResponse(utils.get_success(), content_type="application/json")
    else:
        return HttpResponse(utils.get_failure(), content_type="application/json")


@login_required
def admin_category_save(request):
    if request.method == 'POST':
        try:
            pk = request.POST['mid']
            name = request.POST['cname']
            if utils.isEmpty(pk):
                Category.objects.create(name=name)
                return HttpResponse(utils.get_success(), content_type="application/json")
            else:
                category = get_object_or_404(Category, pk=request.POST['mid'])
                category.name = name
                category.save()
                return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")


@login_required
def admin_tag_delete(request):
    if request.method == 'POST':
        tag = get_object_or_404(Tag, pk=request.POST['mid'])
        if tag is None:
            return HttpResponse(utils.get_failure_with_msg("分类不存在"), content_type="application/json")
        else:
            tag.delete()
            return HttpResponse(utils.get_success(), content_type="application/json")
    else:
        return HttpResponse(utils.get_failure(), content_type="application/json")


class LoginRequiredMixin(object):
    """
    登陆限定，并指定登陆url
    """

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url=settings.LOGIN_URL)


# @login_required
class AdminComment(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'admin/comment_list.html'
    context_object_name = 'comment_list'
    paginate_by = 20

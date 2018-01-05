#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 发布文章


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from BlogProject import settings
from blog.models import Post, Category, Tag
from blogAdmin import utils
from blogAdmin import file_manager


@login_required
def article_publish(request):
    qi_niu = settings.QINIU_BUCKET_DOMAIN
    if settings.QINIU_SECURE_URL:
        qi_niu = 'https://' + qi_niu
    else:
        qi_niu = 'http://' + qi_niu
    return render(request, 'admin/article_edit.html',
                  context={'token': file_manager.get_qiniu_token(), 'attach_url': qi_niu})


# 修改
@login_required
def article_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        pk = request.POST['pk']
        tags = request.POST['tags']
        categories = request.POST['categories']
        if not pk.strip():
            try:
                post = Post.objects.create(title=title, body=content)
                # tag 整理
                save_post_tag(tags, post)
                # 分类
                save_post_categories(categories, post)
                return HttpResponse(utils.get_success(), content_type="application/json")
            except:
                return HttpResponse(utils.get_failure(), content_type="application/json")
        else:
            try:
                post = get_object_or_404(Post, pk=pk)
                post.title = title
                post.body = content
                post.save()
                # 清空post的tag
                post.tags.clear()
                save_post_tag(tags, post)
                # 分类
                # post.category.clean()
                save_post_categories(categories, post)
                return HttpResponse(utils.get_success(), content_type="application/json")
            except:
                return HttpResponse(utils.get_failure(), content_type="application/json")


# 不能加 login_required 否则报错
def save_post_tag(tags, post):
    # tag 整理
    if tags.strip():
        tag_list = tags.split(",")
        for tag in tag_list:
            post_tag = Tag.objects.get_or_create(name=tag)
            post.tags.add(post_tag[0])
            post.save()


def save_post_categories(categories, post):
    if categories.strip():
        cate_list = categories.split(",")
        for cate in cate_list:
            post_cate = Category.objects.get_or_create(name=cate)
            post.category = post_cate[0]
            post.save()


@login_required
def admin_delete(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=request.POST['pk'])
        if post is None:
            return HttpResponse(utils.get_failure_with_msg("文章不存在"),
                                content_type="application/json")
        else:
            post.delete()
            return HttpResponse(utils.get_success(), content_type="application/json")


class LoginRequiredMixin(object):
    """
    登陆限定，并指定登陆url
    """

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url=settings.LOGIN_URL)


# @login_required
class AdminPost(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'admin/article_list.html'
    context_object_name = 'post_list'
    paginate_by = 20


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'admin/article_edit.html'
    context_object_name = 'post'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 发布文章


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Tag, Category
from blogAdmin import utils


@login_required
def article_publish(request):
    return render(request, 'admin/article_edit.html')


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

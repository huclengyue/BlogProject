#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from BlogProject.settings import QINIU_SECURE_URL, QINIU_BUCKET_DOMAIN
from blogAdmin import file_manager, utils
# 分页数
from blogAdmin.models import Attach

ONE_PAGE_OF_DATA = 18


@login_required
def attach_list(request):
    if request.method == 'GET':
        qi_niu = QINIU_BUCKET_DOMAIN
        if QINIU_SECURE_URL:
            qi_niu = 'https://' + qi_niu
        else:
            qi_niu = 'http://' + qi_niu
            # page
        paginator = Paginator(file_manager.get_file(), 18)
        try:
            page = request.GET.get('page', 1)
            posts = paginator.page(page)
            # has_next              是否有下一页
            # next_page_number      下一页页码
            # has_previous          是否有上一页
            # previous_page_number  上一页页码
            # object_list           分页之后的数据列表，已经切片好的数据
            # number                当前页
            # paginator             paginator对象
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        content = {'attach_url': qi_niu,
                   'max_file_size': 20,
                   'token': file_manager.get_qiniu_token(),
                   'file_list': posts}
        return render(request, 'admin/attach.html', context=content)


@login_required
def admin_attach_refresh(request):
    if request.method == 'POST':
        try:
            file_manager.get_file(mast=True)
            return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")


@login_required
def admin_attach_upload(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.POST['info[response]'])
            print(info['key'])
            return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")

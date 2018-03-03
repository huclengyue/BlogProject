#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import time
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
import random
from BlogProject.settings import QINIU_SECURE_URL, QINIU_BUCKET_DOMAIN
from blogAdmin import file_manager, utils
# 分页数
from blogAdmin.models import Attach

ONE_PAGE_OF_DATA = 18

if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
_MAX_CSRF_KEY = 18446744073709551616  # 2 << 63


def _get_new_submit_key():
    return md5_constructor("%s%s" % (randrange(0, _MAX_CSRF_KEY), settings.SECRET_KEY)).hexdigest()


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
            if 'info[response]' in request.POST:
                info = json.loads(request.POST['info[response]'])
                key = info['key']
            else:
                key = request.POST['info[key]']
            Attach.objects.create(key=key, created_time=int(time.time()))
            print(key)
            return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")


# 删除
def admin_attach_delete(request):
    if request.method == 'POST':
        try:
            pk = json.loads(request.POST['pk'])
            attach = Attach.objects.get(pk=pk)
            if attach is None:
                return HttpResponse(utils.get_failure_with_msg('文件不存在'),
                                    content_type="application/json")
            else:
                code = file_manager.delete_file(attach.key)
                # rec 为none 时 删除失败 length == 0 时 删除成功
                if code == 200 or code == 612:
                    attach.delete()
                    return HttpResponse(utils.get_success(), content_type="application/json")
                elif code == 599:
                    return HttpResponse(utils.get_failure_with_msg('服务端操作失败，请重试'),
                                        content_type="application/json")
                else:
                    return HttpResponse(utils.get_failure(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")

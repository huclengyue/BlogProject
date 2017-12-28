#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from blogAdmin import utils


@login_required
def admin_profile(request):
    if request.method == 'GET':
        return render(request, 'admin/profile.html')
    elif request.method == 'POST':
        try:
            user = request.user
            user.nickname = request.POST['nickname']
            user.email = request.POST['email']
            user.save()
            return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")


@login_required
def admin_password(request):
    if request.method == 'POST':
        try:
            old = request.POST['old_password']
            pwd = request.POST['password']
            pwd2 = request.POST['repass']
            if request.user.is_authenticated:
                user = authenticate(username=request.user.username, password=old)
                if user is not None and user.is_active:
                    if pwd == pwd2:
                        user.set_password(pwd)
                        user.save()
                        return HttpResponse(utils.get_success(), content_type="application/json")
                    else:
                        return HttpResponse(utils.get_failure_with_msg("两次密码不一致"), content_type="application/json")
                else:
                    return HttpResponse(utils.get_failure_with_msg("当前用户不存在或被禁用"), content_type="application/json")
            else:
                return HttpResponse(utils.get_failure_with_msg("请登录后在操作"), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")

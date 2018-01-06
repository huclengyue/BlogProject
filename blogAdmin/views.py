from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from blog.models import Friendly, Category, BlogSet
from blogAdmin import utils, file_manager
# Create your views here.
from blogAdmin.models import Attach


@login_required
def admin_index(request):
    # 初始化 当前用户
    user = request.user
    if utils.isEmpty(user.nickname):
        user.nickname = user.username
        user.save()
    # 所以空都将计算为False，非空为True
    if len(Category.objects.filter(name='默认分类')) == 0:
        Category.objects.get_or_create(name='默认分类')
    if Attach.objects.all().count() == 0:
        file_manager.save_to_db()
    return render(request, 'admin/index.html')


def admin_login(request):
    # get得到地址
    if request.method == 'GET':
        if request.user.is_authenticated:
            if utils.isEmpty(request.GET.get('next')):
                return HttpResponseRedirect('/xadmin/')
            else:
                return HttpResponseRedirect(request.GET.get('next'))

        else:
            request.session['login_from'] = request.GET.get('next')
            return render(request, 'registration/login.html')
    elif request.method == 'POST':
        # TODO: 用户登录操作，blablabla
        # 重定向到来源的url
        return HttpResponseRedirect(request.session['login_from'])


@login_required
def admin_links(request):
    return render(request, 'admin/links.html')


@login_required
def admin_links_save(request):
    if request.method == 'POST':
        name = request.POST['name']
        url = request.POST['url']
        sort = request.POST['sort']
        pk = request.POST['pk']
        if not pk.strip():
            Friendly.objects.create(site_name=name, link=url, sort=sort)
            return HttpResponse(utils.get_success(), content_type="application/json")
        else:
            try:
                link = get_object_or_404(Friendly, pk=pk)
                link.site_name = name
                link.link = url
                link.sort = sort
                link.save()
                return HttpResponse(utils.get_success(), content_type="application/json")
            except:
                return HttpResponse(utils.get_failure(), content_type="application/json")


@login_required
def admin_links_delete(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        link = get_object_or_404(Friendly, pk=pk)
        link.delete()
        return HttpResponse(utils.get_success(), content_type="application/json")


@login_required
def admin_setting(request):
    if request.method == 'GET':
        return render(request, 'admin/setting.html')
    elif request.method == 'POST':
        try:
            title = request.POST['site_title']
            description = request.POST['site_description']
            keywords = request.POST['site_keywords']
            if utils.isEmpty(title):
                return HttpResponse(utils.get_failure_with_msg("站点名称不能为空"),
                                    content_type="application/json")
            else:
                blogset = BlogSet.objects.first()
                if blogset is None:
                    blogset = BlogSet.objects.create()
                blogset.site_name = title
                blogset.description = description
                blogset.keywords = keywords
                blogset.save()
                return HttpResponse(utils.get_success(), content_type="application/json")
        except:
            return HttpResponse(utils.get_failure(), content_type="application/json")

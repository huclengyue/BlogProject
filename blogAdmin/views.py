from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView

from BlogProject import settings
from blog.models import Post, Friendly
from blogAdmin import utils


@login_required
def admin_index(request):
    return render(request, 'admin/index.html')


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


@login_required
def admin_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post is None:
        return '''{"msg":"文章不存在","code":-1,"success":false}'''
    else:
        post.delete()
        return '''{"msg":"OK","code":200,"success":True}'''


def admin_login(request):
    # get得到地址
    if request.method == 'GET':
        print(request.GET.get('next'))
        if request.user.is_authenticated:
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


def admin_links_delete(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        link = get_object_or_404(Friendly, pk=pk)
        link.delete()
        return HttpResponse(utils.get_success(), content_type="application/json")


def admin_setting(request):
    return render(request, 'admin/setting.html')

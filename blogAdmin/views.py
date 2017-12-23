from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView

from BlogProject import settings
from blog.models import Post


@login_required
def admin_index(request):
    if request.user.is_authenticated:
        print('Login')
    else:
        print('Login Not')
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
    if request.user.is_authenticated:
        print('Login')
    else:
        print('Login Not')
    return render(request, 'registration/login.html')

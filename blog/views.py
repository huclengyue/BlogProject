# Create your views here.
from django.shortcuts import render, get_object_or_404

from blog.models import Post


# def index(request):
#     # 我们首先把 HTTP请求传了进去，然后render根据第二个参数的值index.html找到这个模板文件并读取模板中的内容。之后render
#     # 根据我们传入的context参数的值把模板中的变量替换为我们传递的变量的值，{{title}}被替换成了context字典中title对应的值，同理
#     # {{welcome}}也被替换成相应的值。
#     return render(request, "index.html", context={"title": "我的博客首页", "welcome": "欢迎访问我的博客"})

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, "blog/index.html", context={"post_list": post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk)
    return render(request, 'blog/detail.html', context={'post': post})

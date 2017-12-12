# Create your views here.
import markdown
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category
from comments.forms import CommentForm

"""
def index(request):
    # 我们首先把 HTTP请求传了进去，然后render根据第二个参数的值index.html找到这个模板文件并读取模板中的内容。之后render
    # 根据我们传入的context参数的值把模板中的变量替换为我们传递的变量的值，{{title}}被替换成了context字典中title对应的值，同理
    # {{welcome}}也被替换成相应的值。
    return render(request, "index.html", context={"title": "我的博客首页", "welcome": "欢迎访问我的博客"})
"""

"""
请使用下方真正的首页视图函数
def index(request):
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
"""


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取评论
    comment_list = post.comment_set.all()
    # 将表单，文章，评论传递
    context = {'post': post, 'form': form, 'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


# 归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


'''
# 分类
这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。
get_object_or_404 函数和 detail 视图中一样，其作用是如果用户访问的分类不存在，则返回一个 404 错误页面以提示用户访问的资源不存在。
然后我们通过 filter 函数过滤出了该分类下的全部文章。同样也和首页视图中一样对返回的文章列表进行了排序。
'''


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

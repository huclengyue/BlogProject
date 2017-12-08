# Create your views here.
from django.shortcuts import render


def index(request):
    # 我们首先把 HTTP请求传了进去，然后render根据第二个参数的值index.html找到这个模板文件并读取模板中的内容。之后render
    # 根据我们传入的context参数的值把模板中的变量替换为我们传递的变量的值，{{title}}被替换成了context字典中title对应的值，同理
    # {{welcome}}也被替换成相应的值。
    return render(request, "index.html", context={"title": "我的博客首页", "welcome": "欢迎访问我的博客"})

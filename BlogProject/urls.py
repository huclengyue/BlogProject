"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from blog.feeds import AllPostsRssFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
    url(r'^xadmin/', include('blogAdmin.urls')),
    url(r'', include('comments.urls')),
    # 记得在顶部引入 AllPostsRssFeed
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
    # search
    url(r'^search/', include('haystack.urls')),
    # 登录模块
    url(r'^users/', include('django.contrib.auth.urls')),
]
handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.page_not_found'

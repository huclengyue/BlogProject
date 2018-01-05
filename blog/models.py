# coding: utf-8

import markdown
from django.conf import settings

from django.db import models
# 分类
from django.urls import reverse
from django.utils.html import strip_tags


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time', 'name']


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time', 'name']


class Post(models.Model):
    # 标题
    title = models.CharField(max_length=70, verbose_name='标题')
    # 正文
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    # 摘要
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True, editable=False, verbose_name='摘要')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    # 分类的外键
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='分类')

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者'
                               , on_delete=models.CASCADE, blank=True, null=True)
    # 内容格式化方式
    fmtType = models.CharField(max_length=20, verbose_name='格式化类型', default='markdown')
    # 阅读量
    views = models.PositiveIntegerField(default=0, editable=False)
    # 别名
    slug = models.CharField(max_length=150, verbose_name='文章别名', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 如果没有摘要
        if not self.excerpt or self.excerpt != strip_tags(md.convert(self.body))[:200]:
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            # self.excerpt = strip_tags(md.convert(self.body))[:200]
            self.excerpt = strip_tags(md.convert(self.body))[:200]
            # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(force_insert, force_update, using,
                               update_fields)

    def get_simple_date(self):
        return self.created_time.strftime("%Y-%m-%d")

    get_simple_date.short_description = u"发布时间"
    short_description = "文章列表"

    class Meta:
        ordering = ['-created_time', 'title']
        verbose_name = '文章'
        verbose_name_plural = '文章'


class BlogSet(models.Model):
    site_name = models.CharField(blank=False, verbose_name='站点名称', max_length=66)
    description = models.TextField(blank=True, verbose_name='站点描述', max_length=150)
    keywords = models.TextField(blank=True, verbose_name='站点关键词', max_length=150)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = '管理内容'
        verbose_name_plural = '站点管理'


class Friendly(models.Model):
    site_name = models.CharField(blank=False, verbose_name='站点名称', max_length=66)
    link = models.CharField(blank=False, verbose_name='链接', max_length=200)
    sort = models.IntegerField(blank=True, default=0, verbose_name='显示顺序')

    def __str__(self):
        return self.site_name

    class Meta:
        ordering = ['sort', 'site_name']
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'


class Catalog(models.Model):
    index = models.IntegerField(blank=True, default=0, verbose_name='显示顺序')
    name = models.CharField(blank=True, verbose_name='分类名称', max_length=20)
    link = models.CharField(blank=False, verbose_name='分类链接', max_length=20)

    class Meta:
        ordering = ['index']
        verbose_name = '目录'
        verbose_name_plural = '目录'

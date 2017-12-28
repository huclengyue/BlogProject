from django.contrib import admin

from blog.models import *


class PostAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['title', 'get_simple_date', 'category']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 30
    # list_editable 设置默认可编辑字段
    list_editable = ['category']
    # 筛选器
    list_filter = ('created_time', 'category', 'tags')  # 过滤器
    search_fields = ('title', 'body')  # 搜索字段
    date_hierarchy = 'created_time'  # 详细时间分层筛选　
    # 多对多字段美化
    filter_horizontal = ('tags',)
    # 页面顶部存在输入框
    save_on_top = True
    fieldsets = (
        ("文章", {'fields': ['title', 'body']}),
        ("其他", {'fields': ['category', 'tags']}),
    )


class BlogAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'description']


class FriendlyAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'link', 'sort']
    fields = (('site_name', 'link', 'sort'),)


class CatalogAdmin(admin.ModelAdmin):
    list_display = ['index', 'name', 'link']
    fields = (('index', 'name', 'link'),)
    list_editable = ['name', 'link']


# 把新增的 PostAdmin 也注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BlogSet, BlogAdmin)
admin.site.register(Friendly, FriendlyAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.site_header = 'Blog后台管理系统'
admin.site.site_title = 'By LengYue'

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.CharField(max_length=300, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Attach(models.Model):
    key = models.CharField(verbose_name='文件名', max_length=200, blank=False)
    file_type = models.CharField(max_length=25, default="image", verbose_name='文件类型')
    created_time = models.IntegerField(default=0, verbose_name='创建时间')
    size = models.IntegerField(default=0, verbose_name='文件大小')

    class Meta:
        ordering = ['-created_time', 'key']
        verbose_name = '附件'
        verbose_name_plural = '附件'

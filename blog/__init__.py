import os

from django.apps import AppConfig

VERBOSE_APP_NAME = u"1-本地服务器资源"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class PrimaryBlogConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME

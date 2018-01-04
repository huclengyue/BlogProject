#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qiniu import Auth, BucketManager

from BlogProject.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME
from blogAdmin.models import Attach
from blogAdmin import utils

qi_niu = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
file_list = []


def get_qiniu_token():
    # 要上传的空间
    # key = str(uuid.uuid1()).replace('-', '')
    token = qi_niu.upload_token(QINIU_BUCKET_NAME, None, 3600)
    return token


# 列举条目
# 前缀
# 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
def get_file(mast=False):
    if mast:
        Attach.objects.all().delete()
        save_to_db()
    else:
        return Attach.objects.all()


def save_to_db():
    bucket = BucketManager(qi_niu)
    # 标记
    ret = bucket.list(QINIU_BUCKET_NAME, prefix=None, marker=None, limit=None, delimiter=None)
    for filekey in ret[0]['items']:
        Attach.objects.create(key=filekey['key'],
                              created_time=utils.intercept_time(filekey['putTime']),
                              size=filekey['fsize'],
                              file_type=filekey['mimeType'])
        # attach.save()


def delete_file(key):
    ret, info = BucketManager(qi_niu).delete(QINIU_BUCKET_NAME, key)
    return ret

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

from qiniu import Auth, BucketManager

from BlogProject.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME

q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


def get_qiniu_token():
    # 要上传的空间
    key = str(uuid.uuid1()).replace('-', '')
    token = q.upload_token(QINIU_BUCKET_NAME, key, 3600)
    return token


# 列举条目
def get_file(limit):
    bucket = BucketManager(q)
    # 要上传的空间
    key = str(uuid.uuid1()).replace('-', '')
    # 前缀
    prefix = None
    # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
    delimiter = None
    # 标记
    marker = None
    ret = bucket.list(QINIU_BUCKET_NAME, prefix, marker, limit, delimiter)
    return ret[0]
    # for r in ret[0].get('items'):
    #     print(r.get('key'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import xpinyin


def get_pinyin(chinese):
    p = xpinyin.Pinyin()
    return p.get_pinyin(chinese).replace(" ", "-").replace("-、", "")


def get_success():
    return json.dumps({"msg": "OK", "code": 200, "success": True})


def get_failure():
    return json.dumps({"code": -1, "success": False})


def get_failure_with_msg(msg):
    return json.dumps({'msg': msg, "code": -1, "success": False})


def isEmpty(string):
    if string == '' and string != 'None':
        return True
    else:
        return False


def intercept_time(time):
    return int(str(time)[:10])

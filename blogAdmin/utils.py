#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def get_success():
    return json.dumps({"msg": "OK", "code": 200, "success": True})


def get_failure():
    return json.dumps({"code": -1, "success": False})

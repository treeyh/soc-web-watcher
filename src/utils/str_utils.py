# -*- encoding: utf-8 -*-

import json


def json_encode(obj):
    return json.dumps(obj, ensure_ascii=False)

def json_decode(json_str):
    return json.loads(json_str)
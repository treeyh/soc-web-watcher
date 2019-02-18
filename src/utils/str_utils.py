# -*- encoding: utf-8 -*-

import json
from typing import Union, Any

def json_encode(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

def json_decode(json_str: Union[str, bytes]) -> Any:

    if isinstance(json_str, (str, type(None))):
        return json.loads(json_str)

    if not isinstance(json_str, bytes):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(json_str))
    return json.loads(json_str.decode("utf-8"))
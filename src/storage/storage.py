# -*- coding: utf-8 -*-

import codecs
import time
import json


def save(file_path, content):
    content_str = json.JSONEncoder(ensure_ascii=False).encode(content)

    suffix = time.strftime("%Y%m%d_%H%M%S")
    file_name = file_path + "_" + suffix + ".json"

    with codecs.open(file_name, "w+", 'utf-8') as f:
        f.write(content_str)

    print("file saved", file_name)

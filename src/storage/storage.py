# -*- coding: utf-8 -*-

import time
import json


def save(file_path, content):
    content_str = json.JSONEncoder().encode(content)

    suffix = time.strftime("%Y%m%d_%H%M%S")
    file_name = file_path + "_" + suffix + ".json"

    with open(file_name, "w+") as f:
        f.write(content_str)

    print("file saved", file_name)

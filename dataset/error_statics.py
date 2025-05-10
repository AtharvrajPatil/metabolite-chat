import os
import json


def duplicate_disease(file_path):
    r = open(file_path, encoding="utf-8")
    orginal_data = json.load(file_path)
    r.close()
    results = []
    strange_str = ""
    for key in orginal_data:
        data_detail = orginal_data[key]
        description = strange_str
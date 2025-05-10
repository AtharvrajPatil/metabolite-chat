import json
import os

length_statistic = {}

result = {}
result_json_path = "dataset_info.json"
dataset_detail_path = "metabolites_detail_full.json"
with open(dataset_detail_path, "r", encoding="utf-8") as r:
    origin_dataset = json.load(r)

metabolite_indexes = origin_dataset.keys()
result['total_count'] = len(metabolite_indexes)
for index in metabolite_indexes:
    metabolite_detail = origin_dataset[index]
    description = metabolite_detail["description"]
    if isinstance(description, str) and len(description) > 4:
        description_words = description.split(" ")
        if str(len(description_words)) in length_statistic.keys():
            length_statistic[str(len(description_words))] += 1
        else:
            length_statistic[str(len(description_words))] = 1

    for key in metabolite_detail.keys():
        detail = metabolite_detail[key]
        if (key == "description" and not isinstance(detail, str)) or detail == "none":
            continue
        else:
            if key in result.keys():
                result[key] += 1
            else:
                result[key] = 1

with open(result_json_path, "w", encoding="utf-8") as w:
    json.dump(result, w, indent=2, ensure_ascii=False)

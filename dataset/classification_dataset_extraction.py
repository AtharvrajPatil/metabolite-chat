import json


detail_path = "metabolites_detail_full.json"
properties = ["cellular_locations", "biospecimen_locations", "diseases", "tissue_locations"]
categories_dict_file = "categories_index.json"


def class_dict_generate():
    with open(detail_path, "r", encoding="utf-8") as r:
        data = json.load(r)
    result_dict = {p: {"count": 0} for p in properties}
    for index in data.keys():
        detail = data[index]
        for p in properties:
            if p in detail.keys():
                p_detail = detail[p]
                if isinstance(p_detail, list):
                    for p_name in p_detail:
                        if p_name not in result_dict[p].keys():
                            result_dict[p][p_name] = result_dict[p]['count']
                            result_dict[p][str(result_dict[p]['count'])] = p_name
                            result_dict[p]['count'] += 1
                elif "none" not in p_detail:
                    p_name = p_detail
                    if p_name not in result_dict[p].keys():
                        result_dict[p][p_name] = result_dict[p]['count']
                        result_dict[p][str(result_dict[p]['count'])] = p_name
                        result_dict[p]['count'] += 1
    with open(categories_dict_file, "w", encoding="utf-8") as w:
        json.dump(result_dict, w, indent=4, ensure_ascii=False)


def categories_statistic():
    with open(detail_path, "r", encoding="utf-8") as r:
        data = json.load(r)
    result_dict = {p: [0, 0] for p in properties}
    for index in data.keys():
        detail = data[index]
        for p in properties:
            if p in detail.keys():
                p_detail = detail[p]
                if isinstance(p_detail, list):
                    result_dict[p][1] += 1
                if "none" not in p_detail:
                    result_dict[p][0] += 1
    print(result_dict)


if __name__ == "__main__":
    # categories_statistic()
    class_dict_generate()
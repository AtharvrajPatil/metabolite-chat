import json

limit_number = 100

def server_comparision():
    origin_data_path = "/data2/Dingcheng/projects/data_crawl/metabolites_detail_full.json"
    rewrote_data_path = "/data2/Dingcheng/projects/data_crawl/metabolites_detail_full_rewrite.json"
    result_path = "/data2/Dingcheng/projects/data_crawl/comparison.json"

    with open(origin_data_path, "r", encoding="utf-8") as r:
        origin_data = json.load(r)

    with open(rewrote_data_path, "r", encoding="utf-8") as r:
        rewrote_data = json.load(r)

    result = {}
    origin_data_keys = list(origin_data.keys())
    rewrote_data_keys = list(rewrote_data.keys())

    for i in range(limit_number):
        metabolite_id = origin_data_keys[i]
        origin_detail = origin_data[metabolite_id]
        rewrote_detail = rewrote_data[metabolite_id]
        result[metabolite_id] = {}
        result[metabolite_id]['smiles'] = origin_detail['smiles']
        result[metabolite_id]['origin_description'] = origin_detail['description']
        result[metabolite_id]['rewrote_description'] = rewrote_detail['description']

    with open(result_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def local_comparision():
    origin_data_path = "comparison.json"
    rewrote_data_path = "metabolites_detail_full_rewrite.json"
    result_path = "final_comparison.json"

    with open(origin_data_path, "r", encoding="utf-8") as r:
        origin_data = json.load(r)

    with open(rewrote_data_path, "r", encoding="utf-8") as r:
        rewrote_data = json.load(r)

    result = {}
    origin_data_keys = list(origin_data.keys())
    rewrote_data_keys = list(rewrote_data.keys())

    for i in range(limit_number):
        metabolite_id = origin_data_keys[i]
        origin_detail = origin_data[metabolite_id]
        rewrote_detail = rewrote_data[metabolite_id]
        result[metabolite_id] = {}
        result[metabolite_id]['smiles'] = origin_detail['smiles']
        result[metabolite_id]['origin_description'] = origin_detail['origin_description']
        result[metabolite_id]['deepseek_14b_rewrote'] = origin_detail['rewrote_description'].split('<summary>')[-1]
        result[metabolite_id]['gpt_4_mini_rewrote'] = rewrote_detail['description']

    with open(result_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)



def examples_get(file="examples_to_show_.json", save_path="examples_to_show.json"):
    new_dict = {}
    with open(file, "r", encoding="utf-8") as r:
        data = json.load(r)
    for key, detail in data.items():
        if len(detail) >= 4:
            new_dict[key] = detail
    with open(save_path, "w", encoding="utf-8") as w:
        json.dump(new_dict, w, ensure_ascii=False, indent=4)
    pass


if __name__ == "__main__":
    # local_comparision()
    examples_get()
import json

rewrite_path = "metabolites_detail_full_rewrite.json"
origin_path = "metabolites_detail_full.json"
word_length_limit = 150

def origin_file_statistic(file_path=origin_path):
    # word_length_limit = 120
    max_words = 0
    valid_description_count = 0
    invalid_description_count = 0
    with open(file_path, "r", encoding="utf-8") as r:
        data = json.load(r)
    metabolite_ids = list(data.keys())
    for metabolite_id in metabolite_ids:
        detail = data[metabolite_id]
        description = detail["description"]
        if check_valid_description(description):
            words_count = len(description.split(" "))
            if words_count > word_length_limit:
                invalid_description_count += 1
                continue
            if words_count > max_words:
                max_words = words_count
            valid_description_count += 1
        else:
            invalid_description_count += 1
    print(f"max_words_count:{max_words}")
    print(
        f"invalid_description count:{invalid_description_count} out of {valid_description_count + invalid_description_count}")

def check_valid_description(description):
    if isinstance(description, str) and len(description) > 4:
        return True
    return False


def rewrite_file_statistic(file_path=rewrite_path):
    think_tag = "</think>"
    # word_length_limit = 150
    max_words = 0
    valid_description_count = 0
    invalid_description_count = 0
    with open(file_path, "r", encoding="utf-8") as r:
        data = json.load(r)
    metabolite_ids = list(data.keys())
    for metabolite_id in metabolite_ids:
        detail = data[metabolite_id]
        description = detail["description"]
        if check_valid_description(description) and think_tag in description:
            description = description.split(think_tag)[-1]
            words_count = len(description.split(" "))
            if words_count > word_length_limit:
                invalid_description_count += 1
                continue
            if words_count > max_words:
                max_words = words_count
            valid_description_count += 1
        else:
            invalid_description_count += 1
    print(f"max_words_count:{max_words}")
    print(f"invalid_description count:{invalid_description_count} out of {valid_description_count + invalid_description_count}")

if __name__ == "__main__":
    origin_file_statistic()
    rewrite_file_statistic()
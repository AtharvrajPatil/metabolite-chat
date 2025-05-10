import json
import random

random.seed(42)

data_path = "metabolites_qa_description_only.json"

with open(data_path, 'r', encoding='utf-8') as file:
    data_dict = json.load(file)

keys = list(data_dict.keys())
random.shuffle(keys)

train_size = int(len(keys) * 0.7)
valid_size = int(len(keys) * 0.2)
test_size = len(keys) - train_size - valid_size

train_keys = keys[:train_size]
valid_keys = keys[train_size:train_size + valid_size]
test_keys = keys[train_size + valid_size:]

train_set = {key: data_dict[key] for key in train_keys}
valid_set = {key: data_dict[key] for key in valid_keys}
test_set = {key: data_dict[key] for key in test_keys}

with open(data_path.split(".")[0] + "_train.json", 'w', encoding='utf-8') as file:
    json.dump(train_set, file, ensure_ascii=False, indent=4)

with open(data_path.split(".")[0] + "_val.json", 'w', encoding='utf-8') as file:
    json.dump(valid_set, file, ensure_ascii=False, indent=4)

with open(data_path.split(".")[0] + "_test.json", 'w', encoding='utf-8') as file:
    json.dump(test_set, file, ensure_ascii=False, indent=4)

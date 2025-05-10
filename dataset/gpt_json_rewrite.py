import json

json_file = "human_test_gpt_4o_full.json"

with open(json_file, "r", encoding="utf-8") as r:
    data = json.load(r)

for key in list(data.keys()):
    temp_data = []
    temp_questions = []
    for item in data[key]:
        if item[0] in temp_questions:
            continue
        else:
            temp_data.append(item)
            temp_questions.append(item[0])
    data[key] = temp_data

with open("human_test_gpt_4o.json", "w", encoding="utf-8") as w:
    json.dump(data, w, indent=4)
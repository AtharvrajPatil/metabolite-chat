import regex as re
import json


def replace_tg_patterns(description):
    if isinstance(description, str):
        # pattern = r'\b[A-Za-z]+\([^)]*\)'
        pattern = r'\b[A-Z]{2,3}(?:-[A-Za-z]+)?\((?![^()]*[\[\]])(?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)'
        description = re.sub(pattern, '<metabolite>', description)
        pattern_post = r'\<metabolite\>\[rac\]'
        description = re.sub(pattern_post, "<metabolite>", description)
        return description
    return description


with open('metabolites_detail_full.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

for entry_id, entry_data in data.items():
    if isinstance(entry_data, dict) and "description" in entry_data:
        entry_data["description"] = replace_tg_patterns(entry_data["description"])

with open('updated_metabolites.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("The descriptions have been updated and saved to 'modified_data.json'.")

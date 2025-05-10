import json
import random

index_path = "categories_index.json"
properties = ["cellular_locations", "biospecimen_locations", "diseases", "tissue_locations"]
evaluation_file_path = "human_test.json"
classification_QA_file = "human_test_classification.json"
with open(index_path, "r", encoding="utf-8") as r:
    properties_index = json.load(r)
with open(evaluation_file_path, "r", encoding="utf-8") as r:
    qa_result = json.load(r)
properties_names_set = {p:set(properties_index[p][str(i)] for i in range(properties_index[p]['count'])) for p in properties}


def regenerate_single_qa(question, answer) -> (str, str):
    property = property_classify_by_question(question)
    answer = extract_properties_from_target(answer)
    if property in ["cellular_locations", "biospecimen_locations"]:
        question = f"What are the {property.replace('_', ' ')} of this metabolite? Choose from the locations listed as below(it may have one or multiple correct choices):\n{properties_names_set[property]}"
    elif property == "diseases":
        contain_real_answer = True if random.random() >= 0.5 else False
        if contain_real_answer:
            diseases = answer
            answer = "yes"
        else:
            diseases = random.choice(list(properties_names_set[property] - set(answer)))
            answer = "no"
        question = f"Predict whether this metabolite is associated with {diseases}. Answer in yes or no."
    elif property == "tissue_locations":
        question = f"What are the {property.replace('_', ' ')} of this metabolite? Choose from the locations listed as below(it may have one or multiple correct choices):\n{properties_names_set[property]}"
    return question, answer

def property_classify_by_question(question: str):
    if "cell" in question:
        return "cellular_locations"
    elif "bio-specimen" in question:
        return "biospecimen_locations"
    elif "tissue" in question:
        return "tissue_locations"
    elif "disorders" in question:
        return "diseases"
    else: return "else"


def extract_properties_from_target(target: str):
    target = target.replace("\'", '')
    target = target.replace("and ", '')
    if "is " in target:
        target = target.split("is ")[1]
        target = target[:-1]
        return [target]
    else:
        target = target.split("are ")[1]
        target = target[:-1].split(" ")
        return target


for smiles in list(qa_result.keys()):
    qa_data = qa_result[smiles]
    tmp_qa_data = []
    for qa_pair in qa_data:
        question, ground_truth, answer = qa_pair
        property = property_classify_by_question(question)
        if property in properties:
            question, ground_truth = regenerate_single_qa(question, ground_truth)
        tmp_qa_data.append([question, ground_truth])
    qa_result[smiles] = tmp_qa_data

with open(classification_QA_file, "w", encoding="utf-8") as w:
    json.dump(qa_result, w, indent=4)

import random
import json
from tqdm import trange


def random_split(origin_list: list):
    number = random.choice(list(range(1, len(origin_list))))
    question_set = random.sample(origin_list, number)
    answer_set = list(set(origin_list) - set(question_set))
    return question_set, answer_set


def description_qa_generate(description: str) -> list:
    choices = list(range(9))
    choice = random.choice(choices)
    if choice == 0:
        question = "Please describe this metabolite."
    elif choice == 1:
        question = "Could you give me some information about this metabolite?"
    elif choice == 2:
        question = "What is the description of this?"
    elif choice == 3:
        question = "describe it"
    elif choice == 4:
        question = "what is this?"
    elif choice == 5:
        question = "tell me about it"
    elif choice == 6:
        question = "For this metabolite, what do you have in mind?"
    elif choice == 7:
        question = "can you introduce this for me?"
    else:
        question = "Give me an introduction of this metabolite"

    return [question, description]


def cellular_location_qa_generate(locations) -> list:
    choices = list(range(3))
    choice = random.choice(choices)
    if choice == 0:
        question = "what is/are the cellular location/locations of this metabolite?"
    elif choice == 1:
        question = "where is this metabolite in cell?"
    else:
        question = "I wonder in which part of a cell it may be located?"

    if isinstance(locations, str):
        return [question, f"One possible location is \'{locations}.\'"]
    else:
        choice = random.choice(choices)
        if choice >= len(choices) - 1:
            q_set, a_set = random_split(locations)
            question = f"Except for cellular locations like \'{format_list(q_set)}\', where else this metabolite may show up in cell?"
            answer = f"You may also find it at \'{format_list(a_set)}\' ."
        else:
            answer = f"Possible locations are \'{format_list(locations)}\'."
        return [question, answer]


def biospecimen_location_qa_generate(locations) -> list:
    choices = list(range(3))
    choice = random.choice(choices)
    if choice == 0:
        question = "what is/are the biospecimen location/locations of this metabolite?"
    elif choice == 1:
        question = "where can I find this metabolite in bio-specimen?"
    else:
        question = "I wonder in which bio-specimen it may be located?"

    if isinstance(locations, str):
        return [question, f"One possible location is {locations}."]
    else:
        choice = random.choice(choices)
        if choice >= len(choices) - 1:
            q_set, a_set = random_split(locations)
            question = f"Except for bio-specimen like \'{format_list(q_set)}\', what else biospecimen may contain this?"
            answer = f"You may also find it at \'{format_list(a_set)}\' ."
        else:
            answer = f"Possible locations are \'{format_list(locations)}.\'"
        return [question, answer]


def tissue_location_qa_generate(locations) -> list:
    choices = list(range(3))
    choice = random.choice(choices)
    if choice == 0:
        question = "what is/are the tissue location/locations of this metabolite?"
    elif choice == 1:
        question = "where can I find this metabolite in tissue?"
    else:
        question = "I wonder in which tissue it will be located?"

    if isinstance(locations, str):
        return [question, f"One possible location is \'{locations}\'."]
    else:
        choice = random.choice(choices)
        if choice >= len(choices) - 1:
            q_set, a_set = random_split(locations)
            question = f"Except for tissue like \'{format_list(q_set)}\', what else tissue may contain this?"
            answer = f"You may also find it at \'{format_list(a_set)}\' ."
        else:
            answer = f"Possible locations are \'{format_list(locations)}\'."
        return [question, answer]


def diseases_qa_generate(locations) -> list:
    choices = list(range(3))
    choice = random.choice(choices)
    if choice == 0:
        question = "what are the associated disorders and diseases with this metabolite?"
    elif choice == 1:
        question = "Give me a list of disorders and diseases may relate to this."
    else:
        question = "Is there any potential hazards of this?"

    if isinstance(locations, str):
        return [question, f"It may be related to one disease, that is \'{locations}\'."]
    else:
        choice = random.choice(choices)
        if choice >= len(choices) - 1:
            q_set, a_set = random_split(locations)
            question = f"Except for disorders/diseases like \'{format_list(q_set)}\', what else it may related to?"
            answer = f"Maybe \'{a_set}\' ."
        else:
            answer = f"It may be related to {len(locations)} diseases, which are \'{format_list(locations)}\'."
        return [question, answer]


def format_list(items):
    if not items:
        return ""
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return ", ".join(items[:-1]) + f" and {items[-1]}"


def chromatographic_properties_qa_generate(properties) -> list:
    assert isinstance(properties, list)
    values = {}
    for property in properties:
        type = property["Adduct Type"]
        value = property["CCS Value (Å2)"]
        data_soource = property["Data Source"]
        reference = property["Reference"]
        if type in values.keys():
            values[type].append(value)
        else:
            values[type] = [value]
    answer = ""
    for type in values.keys():
        vs = values[type]
        if len(vs) == 1:
            v = vs[0]
            tmp_answer = f"In one experiment who's adduct type is {type}, CCS(Collision Cross Sections) value equals to {v} A^2."
        else:
            tmp_answer = f"In {len(vs)} experiments who's adduct type are {type}, CCS(Collision Cross Sections) value equals to " + format_list(vs) + " (A^2)"
            tmp_answer += ". Notice these value are obtained from different experiments, so you may use them to estimate the real value.\n"
        answer += tmp_answer
    choices = list(range(4))
    choice = random.choice(choices)
    if choice == 0:
        question = f"Please tell me the collision cross sections of this metabolite."
    elif choice == 1:
        question = f"Could you give me some information about the experimental chromatographic properties of this metabolite?"
    elif choice == 2:
        question = f"What is the collision cross sections of this?"
    else:
        question = f"tell me its chromatographic properties."
    return [question, answer]


def molecular_properties_qa_generate(molecular_properties) -> list:
    results = []
    if isinstance(molecular_properties, dict):
        molecular_properties = [molecular_properties]
    for property in molecular_properties:
        choices = list(range(4))
        choice = random.choice(choices)
        if choice == 0:
            question = f"Please tell me the {property['kind']} of this metabolite."
        elif choice == 1:
            question = f"Could you give me some information about the {property['kind']} of this metabolite?"
        elif choice == 2:
            question = f"What is the {property['kind']} of this?"
        else:
            question = f"tell me its {property['kind']}."
        description = f"The {property['kind'].replace('_', ' ')} of this is {property['value']}."
        results.append([question, description])
    return results


def check_property(data: dict, property: str) -> bool:
    if property not in data.keys():
        return False
    detail = data[property]
    if isinstance(detail, str) and detail == "none":
        return False
    if isinstance(detail, dict) and len(detail.keys()) == 0:
        return False
    return True


def generate_qa_file(origin_data: dict, keys: list, file_name: str, dataset_flag: str, qa_pair_per_data: int, filter=False, info=True):
    result = {}
    if info:
        info_dict = {}
        info_dict['metabolites_count'] = 0
        info_dict['description'] = 0
        info_dict['diseases'] = 0
        info_dict['tissue_locations'] = 0
        info_dict['biospecimen_locations'] = 0
        info_dict['cellular_locations'] = 0
        info_dict['experimental_chromatographic_properties'] = 0
        info_dict['experimental_molecular_properties'] = 0
    for j in trange(len(keys)):
        key = keys[j]
        details = origin_data[key]
        smiles = details['smiles']
        if not isinstance(smiles, str):
            continue
        temp_data = []
        for i in range(qa_pair_per_data):
            if check_property(details, "description"):
                temp_data.append(description_qa_generate(details["description"]))
                if info:
                    info_dict['description'] += 1
            if check_property(details, "diseases"):
                temp_data.append(diseases_qa_generate(details[ "diseases"]))
                if info:
                    info_dict['diseases'] += 1
            if check_property(details, "tissue_locations"):
                temp_data.append(tissue_location_qa_generate(details["tissue_locations"]))
                if info:
                    info_dict['tissue_locations'] += 1
            if check_property(details, "biospecimen_locations"):
                temp_data.append(biospecimen_location_qa_generate(details["biospecimen_locations"]))
                if info:
                    info_dict['biospecimen_locations'] += 1
            if check_property(details, "cellular_locations"):
                temp_data.append(cellular_location_qa_generate(details["cellular_locations"]))
                if info:
                    info_dict['cellular_locations'] += 1
            if check_property(details, "experimental_chromatographic_properties"):
                temp_data.append(chromatographic_properties_qa_generate(details["experimental_chromatographic_properties"]))
                if info:
                    info_dict['experimental_chromatographic_properties'] += 1
            if check_property(details, "experimental_molecular_properties"):
                temp_data.extend(molecular_properties_qa_generate(details["experimental_molecular_properties"]))
                if info:
                    info_dict['experimental_molecular_properties'] += 1
        result[smiles] = temp_data
    print(f"{dataset_flag}set: {len(result)} items")
    if info:
        info_dict['metabolites_count'] = len(result)
        info_dict['triplets_count'] = sum(len(item) for item in result.values())
    with open(file_name + f"_{dataset_flag}.json", 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    if info:
        with open(file_name + f"_{dataset_flag}_info.json", 'w', encoding='utf-8') as file:
            json.dump(info_dict, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # settings
    random.seed(42)
    qa_pair_per_data = 1
    sample_number = 0
    train_proportion = 1
    val_proportion = 0
    test_proportion = 0
    origin_data_path = "metabolites_detail_full.json"
    output_data_file_name = "metabolites_v1"
    filter = False

    with open(origin_data_path, 'r', encoding='utf-8') as file:
        data_dict = json.load(file)

    keys = list(data_dict.keys())
    if sample_number != 0:
        keys = keys[:sample_number]
    random.shuffle(keys)

    train_size = int(len(keys) * train_proportion)
    valid_size = int(len(keys) * val_proportion)
    test_size = len(keys) - train_size - valid_size

    train_keys = keys[:train_size]
    valid_keys = keys[train_size:train_size + valid_size]
    test_keys = keys[train_size + valid_size:]

    generate_qa_file(origin_data=data_dict, keys=train_keys, file_name=output_data_file_name, dataset_flag='train',
                     qa_pair_per_data=qa_pair_per_data, filter=filter)
    # generate_qa_file(origin_data=data_dict, keys=valid_keys, file_name=output_data_file_name, dataset_flag='val',
    #                  qa_pair_per_data=qa_pair_per_data, filter=filter)
    # generate_qa_file(origin_data=data_dict, keys=test_keys, file_name=output_data_file_name, dataset_flag='test',
    #                  qa_pair_per_data=qa_pair_per_data, filter=filter)

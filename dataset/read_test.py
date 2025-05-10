import xml.etree.ElementTree as ET
import json
from tqdm import tqdm


def check_and_get(data:dict, key) -> str:
    if key in data.keys():
        return data[key]
    else:
        return "null"


def remove_namespace(tag):
    # 去掉命名空间部分，返回无命名空间的标签
    if '}' in tag:
        return tag.split('}', 1)[1]  # 去掉大括号以及命名空间部分
    else:
        return tag


def element_to_dict(element):
    # 将元素的属性转为字典
    tag = remove_namespace(element.tag)
    result = {tag: {}}

    for key, value in element.attrib.items():
        # 也去掉属性中的命名空间
        key = remove_namespace(key)
        result[tag][key] = value

    # 处理子元素
    for child in element:
        child_dict = element_to_dict(child)
        child_tag = remove_namespace(child.tag)

        # 如果标签已存在，合并
        if child_tag in result[tag]:
            if isinstance(result[tag][child_tag], list):
                result[tag][child_tag].append(child_dict[child_tag])
            else:
                result[tag][child_tag] = [result[tag][child_tag], child_dict[child_tag]]
        else:
            result[tag][child_tag] = child_dict[child_tag]

    # 处理文本内容
    if element.text and element.text.strip():
        result[tag] = element.text.strip()

    return result


data_path = "hmdb_metabolites.xml"
ET.register_namespace('', 'http://www.hmdb.ca')
output_json_file = "metabolites_class.json"
output_data = []

context = ET.iterparse(data_path, events=("start", "end"))

for event, elem in tqdm(context):
    if event == "end" and elem.tag == '{http://www.hmdb.ca}metabolite':
        accession = elem.find('{http://www.hmdb.ca}accession')
        # if accession is not None and accession.text == 'HMDB0000030':
        #     metabolite_dict = element_to_dict(elem)
        #     print(metabolite_dict)
        #     break  # 找到后可选择停止解析
        if accession is not None:
            try:
                metabolite_dict = element_to_dict(elem)
                metabolite_dict = metabolite_dict['metabolite']
                metabolite_accession = metabolite_dict['accession']
                metabolite_smiles = metabolite_dict['smiles']
                metabolite_detail = {}
                metabolite_detail['name'] = metabolite_dict['name']
                metabolite_detail['id'] = metabolite_accession
                metabolite_detail['smiles'] = metabolite_smiles
                if len(metabolite_dict['taxonomy']) == 0:
                    metabolite_detail['kingdom'] = 'null'
                    metabolite_detail['superclass'] = 'null'
                    metabolite_detail['class'] = 'null'
                    metabolite_detail['subclass'] = 'null'
                    metabolite_detail['direct_parent'] = 'null'
                else:
                    taxonomy = metabolite_dict['taxonomy']
                    metabolite_detail['kingdom'] = check_and_get(taxonomy, 'kingdom')
                    metabolite_detail['superclass'] = check_and_get(taxonomy, 'super_class')
                    metabolite_detail['class'] = check_and_get(taxonomy, 'class')
                    metabolite_detail['subclass'] = check_and_get(taxonomy, 'sub_class')
                    metabolite_detail['direct_parent'] = check_and_get(taxonomy, 'direct_parent')
                # if len(metabolite_dict['biological_properties']['cellular_locations']) > 0:
                #     metabolite_detail['cellular_locations'] = metabolite_dict['biological_properties']['cellular_locations']['cellular']
                # else:
                #     metabolite_detail['cellular_locations'] = "none"
                #
                # if len(metabolite_dict['biological_properties']['biospecimen_locations']) > 0:
                #     metabolite_detail['biospecimen_locations'] = metabolite_dict['biological_properties']['biospecimen_locations']['biospecimen']
                # else:
                #     metabolite_detail['biospecimen_locations'] = "none"
                #
                # if len(metabolite_dict['biological_properties']['tissue_locations']) > 0:
                #     metabolite_detail['tissue_locations'] = \
                #     metabolite_dict['biological_properties']['tissue_locations']['tissue']
                # else:
                #     metabolite_detail['tissue_locations'] = "none"
                #
                # if 'description' in metabolite_dict.keys():
                #     metabolite_detail['description'] = metabolite_dict['description']
                # else:
                #     metabolite_detail['description'] = "none"
                # # for diseases, only save the names.
                #
                # if len(metabolite_dict['diseases']) > 0:
                #     diseases = metabolite_dict['diseases']['disease']
                #     if isinstance(diseases, list):
                #         diseases_name = [item['name'] for item in diseases]
                #     else:
                #         diseases_name = diseases['name']
                #     metabolite_detail['diseases'] = diseases_name
                # else:
                #     metabolite_detail['diseases'] = "none"
                #
                # if len(metabolite_dict['experimental_properties']) > 0 and len(metabolite_dict['experimental_properties']['property']) > 0:
                #     metabolite_detail['experimental_molecular_properties'] = metabolite_dict['experimental_properties']['property']
                # else:
                #     metabolite_detail['experimental_molecular_properties'] = "none"
                # metabolite_detail['smiles'] = metabolite_smiles
                # output_data[metabolite_accession] = metabolite_dict
                output_data.append(metabolite_detail)

                # 清理已解析的元素以节省内存
                elem.clear()
            except Exception as e:
                # print(e)
                metabolite_dict = element_to_dict(elem)
                # print(metabolite_dict)
                elem.clear()

if __name__ == "__main__":
    print(f"total metabolites count: {len(output_data)}")
    w = open(output_json_file, 'w', encoding="utf-8")
    json.dump(output_data, w, indent=2, ensure_ascii=False)
    w.close()

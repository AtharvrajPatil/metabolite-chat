import json
import random

def split_json(input_file, output_train, output_val, output_test):
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取所有键值对的列表
    items = list(data.items())

    # 随机打乱数据
    random.shuffle(items)

    # 按 7:2:1 分割数据
    total = len(items)
    train_split = int(total * 0.7)
    val_split = int(total * 0.9)

    train_items = items[:train_split]
    val_items = items[train_split:val_split]
    test_items = items[val_split:]

    # 转换回字典格式
    train_data = dict(train_items)
    val_data = dict(val_items)
    test_data = dict(test_items)

    # 保存到新的 JSON 文件中
    with open(output_train, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)

    with open(output_val, 'w', encoding='utf-8') as f:
        json.dump(val_data, f, ensure_ascii=False, indent=4)

    with open(output_test, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)

# 示例用法
if __name__ == "__main__":
    input_file = "metabolites_v1_train.json"
    output_train = "train.json"
    output_val = "val.json"
    output_test = "test.json"

    split_json(input_file, output_train, output_val, output_test)
    print("数据已成功分割并保存！")

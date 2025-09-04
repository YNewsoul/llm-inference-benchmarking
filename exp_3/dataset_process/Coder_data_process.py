from datasets import load_dataset
import json

'''
    处理Coder数据集,使其能被脚本使用
'''
dataset = load_dataset("ajibawa-2023/Python-Code-23k-ShareGPT", split="train")

# 转换为目标JSON格式
converted_data = []
for item in dataset:
    converted_item = {
        "id": item["id"],
        "conversations": item["conversations"]
    }
    converted_data.append(converted_item)

# 写入输出JSON文件
output_path = "converted_dataset.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(converted_data, f, indent=2, ensure_ascii=False)

print(f"数据集已成功转换并保存到 {output_path}")
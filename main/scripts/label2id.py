import json

# Load your JSON dataset.
with open("C:/Users/cbsag/OneDrive/Desktop/BioASQ/main/datasets/train_gold.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Collect all unique entity labels from the dataset.
unique_labels = set()
for file_id, content in data.items():
    for entity in content.get("entities", []):
        unique_labels.add(entity["label"])

# Sort the labels to have a consistent order.
unique_labels = sorted(unique_labels)
print("Unique labels in the dataset:", unique_labels)

# Create a label2id dictionary.
# We'll reserve index 0 for "O" (outside any entity),
# then assign indices to "B-<label>" and "I-<label>" for each unique label.
label2id = {"O": 0}
current_index = 1
for label in unique_labels:
    label2id[f"B-{label}"] = current_index
    current_index += 1
    label2id[f"I-{label}"] = current_index
    current_index += 1

# print("label2id mapping:")
with open("C:/Users/cbsag/OneDrive/Desktop/BioASQ/main/outputs/label2id.json", "w", encoding="utf-8") as f:
    json.dump(label2id, f, indent=4, ensure_ascii=False)
# print(label2id)

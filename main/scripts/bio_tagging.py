import json
import re

def apply_bio_tags_using_char_offsets(text, entities):
    """
    Given a text and its entity annotations (with character offsets),
    returns tokens and BIO tags based on character-level annotation.
    """
    # 1. Create a character-level annotation array for the entire text.
    char_tags = ["O"] * len(text)
    for entity in entities:
        ent_start = entity["start_idx"]
        ent_end = entity["end_idx"]
        label = entity["label"]
        # Mark each character in the entity span with its label.
        for i in range(ent_start, ent_end):
            char_tags[i] = label

    # 2. Tokenize the text while keeping track of character offsets.
    tokens = []
    for match in re.finditer(r'\S+', text):
        token = match.group()
        start = match.start()
        end = match.end()
        tokens.append((token, start, end))

    # 3. Project character annotations to tokens to produce BIO tags.
    bio_tags = []
    for token, start, end in tokens:
        # Get the annotations for this token.
        token_labels = char_tags[start:end]
        # If none of the characters are annotated, tag as "O".
        if all(label == "O" for label in token_labels):
            bio_tags.append("O")
        else:
            # Assume all annotated characters share the same label.
            annotated = [lab for lab in token_labels if lab != "O"]
            token_label = annotated[0]
            # Check if the first character of the token marks the beginning of an entity.
            if start == 0 or char_tags[start - 1] != token_label:
                bio_tags.append(f"B-{token_label}")
            else:
                bio_tags.append(f"I-{token_label}")
    
    return tokens, bio_tags

# Load your dataset.
with open("C:/Users/cbsag/OneDrive/Desktop/BioASQ/main/datasets/train_gold.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# This dictionary will hold the BIO tags for each file ID.
all_bio_tags = {}

# Iterate over each file ID in the dataset.
for file_id, content in data.items():
    metadata = content["metadata"]
    entities = content["entities"]
    
    # Extract title and abstract texts.
    title_text = metadata.get("title", "")
    abstract_text = metadata.get("abstract", "")
    
    # Filter entities for title and abstract.
    title_entities = [ent for ent in entities if ent["location"] == "title"]
    abstract_entities = [ent for ent in entities if ent["location"] == "abstract"]
    
    # Process title and abstract to get BIO tags.
    _, title_bio_tags = apply_bio_tags_using_char_offsets(title_text, title_entities)
    _, abstract_bio_tags = apply_bio_tags_using_char_offsets(abstract_text, abstract_entities)
    
    # Save the BIO tags for this file ID.
    all_bio_tags[file_id] = {
        "title_bio_tags": title_bio_tags,
        "abstract_bio_tags": abstract_bio_tags
    }
    
    print(f"Processed file id: {file_id}")

# Write the resulting BIO tags to an output file.
with open("all_bio_tags.json", "w", encoding="utf-8") as f:
    json.dump(all_bio_tags, f, indent=4, ensure_ascii=False)

print("Tagging completed and saved to all_bio_tags.json")

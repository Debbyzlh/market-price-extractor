import json
import pandas as pd

# Load JSON OCR result from your specific file
input_file = "baidu_body_cells-test03.json"
output_file = "extracted_products.csv"

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

def extract_triplets_by_code_width(words_result, max_width=50, max_code_value=1000):
    """
    Extracts (name, code, price) triplets from OCR data using width and numeric filtering on code.

    Args:
        words_result (list): OCR entries from Baidu's output.
        max_width (int): Max pixel width to consider a word as a code.
        max_code_value (int): Upper limit on numeric code value.

    Returns:
        list of dicts: Records containing name, code, and price.
    """
    triplets = []

    for idx in range(len(words_result)):
        cell = words_result[idx]
        width = cell["location"]["width"]
        word = cell["words"].strip()

        if width > max_width:
            continue

        if word.isdigit() and int(word) > max_code_value:
            continue  # skip this code but keep scanning

        try:
            name = words_result[idx - 1]["words"].strip()
            raw_price = words_result[idx + 1]["words"].strip()
            price = raw_price if raw_price.replace(".", "").isdigit() else "NA"

            triplets.append({
                "name": name,
                "code": word,
                "price": price
            })
        except IndexError:
            continue

    return triplets

# Extract and save the data
records = extract_triplets_by_code_width(data["words_result"])
df = pd.DataFrame(records)
df.to_csv(output_file, index=False, encoding="utf-8-sig")
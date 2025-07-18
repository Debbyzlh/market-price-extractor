def extract_iphone_prices_from_json(ocr_json, color_match_path, input_excel_path, product_chosen):
    import pandas as pd
    import json

    # Step 1: load color mapping (e.g., 黑色 → Black)
    if hasattr(color_match_path, "read"):
        color_df = pd.read_excel(color_match_path)
    else:
        color_df = pd.read_excel(str(color_match_path))
    color_map = {
        str(row["Color (CN)"]).strip(): str(row["Color (EN)"]).strip()
        for _, row in color_df.iterrows()
    }
    
    # Step 2: load product data
    if hasattr(input_excel_path, "read"):
        iphone_df = pd.read_excel(input_excel_path, sheet_name="iPhone")
    else:
        iphone_df = pd.read_excel(str(input_excel_path), sheet_name="iPhone")
    iphone_df.columns = iphone_df.columns.str.strip().str.lower()  # ✅ Strip column names FIRST

    # Forward-fill merged cells
    iphone_df[["name", "storsize short desc"]] = iphone_df[["name", "storsize short desc"]].ffill()


    # ✅ Then filter rows
    product_chosen = product_chosen.strip()
    iphone_df = iphone_df[iphone_df["name"].astype(str).str.strip() == product_chosen]
    print("📋 Rows after filtering by product name:", len(iphone_df))  #change

    # Normalize for matching
    iphone_df["storsize short desc"] = iphone_df["storsize short desc"].astype(str).str.lower().str.strip()
    iphone_df["color short desc"] = iphone_df["color short desc"].astype(str).str.lower().str.strip()

    # Step 3: parse OCR JSON
    results = ocr_json["words_result"]
    indexed = [
        {"text": item["words"], "top": item["location"]["top"], "left": item["location"]["left"]}
        for item in results
    ]

    output_rows = []

    for i, item in enumerate(indexed):
        word = item["text"].lower()
        # Fix OCR typos like '512GE' → '512GB'
        word = word.replace("ge", "gb").replace("gd", "gb") 
        word = word.replace(" ", "")

        matched_size = next((s for s in ["256gb", "512gb", "128gb", "1tb"] if s in word), None)
        matched_color_cn = next((cn for cn in color_map if cn in word), None)

        if matched_size and matched_color_cn:
            matched_color_en = color_map[matched_color_cn].lower().strip()

            # Step 4: look ahead for price
            for cand in indexed[i + 1:]:
                price = cand["text"]

                if price.isdigit():
                    print("🔍 Trying to match:")
                    print(f"  - size: '{matched_size}'")
                    print(f"  - color_en: '{matched_color_en}'")
                    print("🧾 Available sizes in Excel:", iphone_df["storsize short desc"].unique())
                    print("🧾 Available colors in Excel:", iphone_df["color short desc"].unique())

                    matched = iphone_df[
                        (iphone_df["storsize short desc"] == matched_size) &
                        (iphone_df["color short desc"] == matched_color_en)
                    ]

                    if not matched.empty:
                        for _, row in matched.iterrows():
                            output_rows.append({
                                "mpn": row["mpn"],
                                "storsize": matched_size,
                                "color_cn": matched_color_cn,
                                "color_en": matched_color_en,
                                "price": price
                            })
                    break

    return output_rows

# # test iphone
# results = extract_iphone_prices_from_json(
#     ocr_json,
#     "color_en_cn_match.xlsx",
#     "SAMPLE excel.xlsx",
#     " 16 Pro MAX"
# )
# for row in results:
#     print(row)


def extract_ipad_prices_from_json(ocr_json, color_match_path, input_excel_path, product_chosen):
    import pandas as pd
    import json
    import streamlit as st

    # Step 1: load color mapping (e.g., 黑色 → Black)
    if hasattr(color_match_path, "read"):
        color_df = pd.read_excel(color_match_path)
    else:
        color_df = pd.read_excel(str(color_match_path))
    color_map = {
        str(row["Color (CN)"]).strip(): str(row["Color (EN)"]).strip()
        for _, row in color_df.iterrows()
    }
    # Handle equivalence: '白色' can mean either 'silver' or 'starlight'
    equivalent_colors = {
        "白色": ["silver", "starlight"]
    }
    
    # Step 2: load product data
    if hasattr(input_excel_path, "read"):
        ipad_df = pd.read_excel(input_excel_path, sheet_name="iPad")
    else:
        ipad_df = pd.read_excel(str(input_excel_path), sheet_name="iPad")
    ipad_df.columns = ipad_df.columns.str.strip().str.lower() 

    # Forward-fill merged cells
    ipad_df[["name", "storsize short desc"]] = ipad_df[["name", "storsize short desc"]].ffill()


    # ✅ Then filter rows
    product_chosen = product_chosen.strip()
    ipad_df = ipad_df[ipad_df["name"].astype(str).str.strip() == product_chosen]
    # print("📋 Rows after filtering by product name:", len(ipad_df))  #change

    # Normalize for matching
    ipad_df["storsize short desc"] = ipad_df["storsize short desc"].astype(str).str.lower().str.strip().str.replace(" ", "")
    # print("🧾 Available sizes in Excel:", ipad_df["storsize short desc"].unique()) #change
    ipad_df["color short desc"] = ipad_df["color short desc"].astype(str).str.lower().str.strip()

    # Step 3: parse OCR JSON
    results = ocr_json["words_result"]
    indexed = [
        {"text": item["words"], "top": item["location"]["top"], "left": item["location"]["left"]}
        for item in results
    ]

    output_rows = []

    for i, item in enumerate(indexed):
        word = item["text"].lower()
        # Fix OCR typos like '512G' → '512GB'
        word = (word.lower()
                .replace(" ", "")
                .replace("ge", "gb")
                .replace("gd", "gb")
                .replace("g", "gb")
                .replace("1tb纳米", "1tb(nano-textureglas)")
                .replace("2tb纳米", "2tb(nano-textureglas)")
                .replace("tb纳米", "tb(nano-textureglas)")
                .replace("纳米", "(nano-textureglas)")
                .replace("（", "(").replace("）", ")")  # fix full-width brackets
        )
        # word = word.replace(" ", "")

        storage_options = [
            "1tb(nano-textureglas)",
            "2tb(nano-textureglas)",
            "256gb", "512gb", "128gb", "1tb", "2tb"
        ]
        storage_options = sorted(storage_options, key=len, reverse=True)
        cleaned_word = word.lower().replace(" ", "").replace("(", "").replace(")", "")
        matched_size = next((s for s in storage_options if s.replace("(", "").replace(")", "") in cleaned_word), None)
        # matched_size = next((s for s in storage_options if s in word.lower().replace(" ", "")), None)
        matched_color_cn = next((cn for cn in color_map if cn in word), None)

        if matched_size and matched_color_cn:
            matched_color_en = color_map[matched_color_cn].lower().strip()
            color_candidates = equivalent_colors.get(matched_color_cn, [matched_color_en])

            # Step 4: look ahead for price
            for cand in indexed[i + 1:]:
                price = cand["text"]

                if price.isdigit():
                    # print("🔍 Trying to match:")
                    # print(f"  - size: '{matched_size}'")
                    # print(f"  - color_en: '{matched_color_en}'")
                    # print("🧾 Available sizes in Excel:", ipad_df["storsize short desc"].unique())
                    # print("🧾 Available colors in Excel:", ipad_df["color short desc"].unique())
                    # st.write("🔍 Trying to match:")
                    # st.write(f"  - size: '{matched_size}'")
                    # st.write(f"  - color_en: '{matched_color_en}'")
                    # st.write(f"  - color_candidates: '{color_candidates}'")
                    # st.write("🧾 Available sizes in Excel:", ipad_df["storsize short desc"].unique())
                    # st.write("🧾 Available colors in Excel:", ipad_df["color short desc"].unique())

                    matched = ipad_df[
                        (ipad_df["storsize short desc"] == matched_size) &
                        (ipad_df["color short desc"].isin(color_candidates))
                    ]

                    if not matched.empty:
                        for _, row in matched.iterrows():
                            output_rows.append({
                                "mpn": row["mpn"],
                                "storsize": matched_size,
                                "color_cn": matched_color_cn,
                                "color_en": matched_color_en,
                                "price": price
                            })
                    break

    return output_rows

# # test ipad
# ipad2_ocr_json = json.load(open("data/ipad2_ocr_result.json"))
# results = extract_ipad_prices_from_json(
#     ipad2_ocr_json,
#     "ipad_color_en_cn_match.xlsx",
#     "SAMPLE excel.xlsx",
#     "iPad Pro 11in  WiFi"
# )

# results
# len(results)



# normalized_word = "1TB纳米黑色".lower().strip().replace(" ", "").replace("（", "(").replace("）", ")")
# normalized_word = normalized_word.replace("1tb纳米", "1tb(nano-textureglas)")
# normalized_word
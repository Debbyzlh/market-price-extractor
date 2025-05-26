import pandas as pd
import json

def map_mpn_to_ocr_price(cpu_excel_path, mpn_code_path, ocr_json_path):
    # Load CPU sheet
    cpu_df = pd.read_excel(cpu_excel_path, sheet_name="CPU")
    
    # Load MPN → Code mapping
    mpn_code_df = pd.read_excel(mpn_code_path)
    mpn_code_map = dict(zip(mpn_code_df["MPN"].astype(str), mpn_code_df["code"].astype(str)))

    # Load OCR JSON
    with open(ocr_json_path, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)["words_result"]

    # Build Code → Price mapping from OCR data
    ocr_code_price = {}
    for i in range(len(ocr_data) - 1):
        code = ocr_data[i]["words"].strip()
        price = ocr_data[i + 1]["words"].strip()

        if code.isalnum() and len(code) <= 4 and price.replace(".", "").isdigit():
            ocr_code_price[code] = price

    # Ensure MPNs are treated as string
    cpu_df["MPN"] = cpu_df["MPN"].astype(str)

    # Map price using MPN → code → price
    cpu_df["未税市场价"] = cpu_df["MPN"].map(
        lambda mpn: ocr_code_price.get(mpn_code_map.get(mpn, ""), "未找到")
    )

    return cpu_df


# df = map_mpn_to_ocr_price(
#     "SAMPLE excel.xlsx",
#     "MPN-code.xlsx",
#     "baidu_body_cells-test04.json"
# )

# df.to_excel("updated_cpu_with_prices.xlsx", index=False)
import streamlit as st
import pandas as pd
import base64
import json
from io import BytesIO
import tempfile
from PIL import Image
from get_json import get_access_token, ocr_image_to_json, is_valid_image
from excel_code_price import map_mpn_to_ocr_price
from iphone_json_to_tbl import extract_iphone_prices_from_json

# Use your API credentials
YOUR_API_KEY = "Xkk7U2sOfAwEKT3BrH4Atucg"
YOUR_SECRET_KEY = "ss2Ki6UWcfuCM58spfKt22hhg8u91WIa"

st.set_page_config(layout="wide", page_title="Market Scanner")

st.info("⚙️ 如果您刚刚唤醒了应用，请耐心等待几秒加载全部功能…")

# App UI
st.title("💻📱 市场价格抓取")

main_tabs = st.tabs(["iPhone", "iPad", "Mac"])

# ---- iPhone Tab Implementation ----
with main_tabs[0]:
    st.header("请确保图片和Excel格式正确")
    uploaded_excel = st.file_uploader("📤 上传带有iPhone表单的Excel文件", type=["xlsx"])
    

    # Upload color mapping Excel
    color_match_file = st.file_uploader("📘 上传 color_en_cn_match.xlsx", type=["xlsx"], key="color_map")
    if not color_match_file:
        st.warning("⚠️ 请上传颜色对照表以启用图片识别功能。")
        st.stop()

    if uploaded_excel:
        df = pd.read_excel(uploaded_excel, sheet_name="iPhone")  # assumes correct sheet
        if "NAME" not in df.columns:
            st.error("❌ iPhone表单中必须包含 'NAME' 列。")
            st.stop()

        if "未税市场价" not in df.columns:
            st.warning("⚠️ 当前Excel中未找到 '未税市场价' 列，价格无法回填。")
        else:
            st.success("✅ 已检测到 '未税市场价' 列。")

        # Step 0: Get distinct product names
        product_names = [str(p) for p in df["NAME"].dropna().unique().tolist()]
        # Step 1: Collect uploaded screenshots for each product
        iphone_tabs = st.tabs(product_names)
        uploaded_image_dict = {}

        for product_name, tab in zip(product_names, iphone_tabs):
            with tab:
                st.subheader(f"📷 上传 {product_name} 的价格截图")

                image_files = st.file_uploader(
                    f"上传截图对应于【{product_name}】（可上传多张）", 
                    type=["jpg", "jpeg", "png"],
                    accept_multiple_files=True,
                    key=f"{product_name}_images"
                )
                uploaded_image_dict[product_name] = image_files
                

        # Step 2: After all uploads, confirm and extract
        if st.button("📤 我已上传所有截图，开始识别并填表"):
            st.info("⏳ 正在处理所有图片...")
            all_results = []

            # Save uploaded Excel and color mapping to temp files
            temp_excel = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_excel.write(uploaded_excel.getvalue())
            temp_excel.flush()
            temp_excel_path = temp_excel.name
            temp_excel.close()

            temp_color = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_color.write(color_match_file.read())
            temp_color.flush()
            temp_color_path = temp_color.name
            temp_color.close()

            # Baidu Token
            token = get_access_token(YOUR_API_KEY, YOUR_SECRET_KEY)
            if not token:
                st.error("❌ 无法获取百度Token")
                st.stop()

            # Process each product's images
            total = sum(len(v) for v in uploaded_image_dict.values())
            processed = 0
            progress = st.progress(0)
            for product_name, image_files in uploaded_image_dict.items():
                if not image_files:
                    st.warning(f"⚠️ 未上传【{product_name}】的截图，跳过。")
                    continue

                for i, img_file in enumerate(image_files):
                    st.write(f"📸 正在处理 {product_name} 的第 {i+1}/{len(image_files)} 张图片")
                    # existing logic...
                    processed += 1
                    progress.progress(processed / total)
                    image_bytes = img_file.getvalue()
                    if not is_valid_image(image_bytes):
                        continue
                    ocr_json = ocr_image_to_json(image_bytes, token)
                    if "words_result" not in ocr_json:
                        continue
                    extracted = extract_iphone_prices_from_json(
                        ocr_json,
                        temp_color_path,
                        temp_excel_path,
                        product_name
                    )
                    all_results.extend(extracted)

            # Step 3: Write back to Excel
            if all_results:
                df_all = pd.DataFrame(all_results)
                before = len(df_all)
                df_all = df_all.drop_duplicates(subset="mpn", keep="last")  # or keep="first"
                after = len(df_all)
                st.info(f"🔍 去重后剩余 {after} 条记录（移除 {before - after} 条重复项）")
                st.success(f"✅ 累计提取 {len(df_all)} 条记录")
                st.dataframe(df_all)

                uploaded_excel.seek(0)
                iphone_df = pd.read_excel(uploaded_excel, sheet_name="iPhone")
                iphone_df.columns = iphone_df.columns.str.strip()
                iphone_df[["NAME", "Storsize Short Desc"]] = iphone_df[["NAME", "Storsize Short Desc"]].ffill()
                iphone_df["MPN"] = iphone_df["MPN"].astype(str).str.strip()

                for _, row in df_all.iterrows():
                    iphone_df.loc[iphone_df["MPN"] == row["mpn"], "未税市场价"] = row["price"]

                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    iphone_df.to_excel(writer, sheet_name="iPhone", index=False)
                buffer.seek(0)

                st.download_button(
                    label="📥 下载完整价格Excel",
                    data=buffer,
                    file_name="iPhone_价格总表.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("⚠️ 未提取到任何价格数据。")


# Placeholder tabs
for tab in main_tabs[1:2]:
    with tab:
        st.info("敬请期待！")

# ---- Mac Tab Implementation ----
with main_tabs[2]:
    st.header("请确保图片和Excel格式正确")

    uploaded_img = st.file_uploader("1. 上传Mac价格截图", type=["jpg", "jpeg", "png"])   

    uploaded_excel = st.file_uploader("2. 上传带有CPU表单的Excel文件（文件名必须全英文）", type=["xlsx"])
    uploaded_mpn_code = st.file_uploader("3. 上传 MPN-code.xlsx", type=["xlsx"])

    if uploaded_img and uploaded_excel and uploaded_mpn_code:
        if st.button("📤 识别 + 填表"):
            with st.spinner("🎯 正在处理..."):
                import tempfile
                import json

                # Save image to bytes
                image_bytes = uploaded_img.getvalue()


                # Validate image format before OCR
                if not is_valid_image(image_bytes):
                    st.error("❌ 上传的图片格式不被识别，可能不是有效的 JPG/PNG。请尝试重新导出或截图。")
                    st.stop()

                # Get Baidu token and call OCR
                token = get_access_token(YOUR_API_KEY, YOUR_SECRET_KEY)
                if not token:
                    st.error("无法获取百度Token，请检查密钥。")
                    st.stop()

                try:
                    json_data = ocr_image_to_json(image_bytes, token)
                    if "words_result" not in json_data:
                        st.write(json_data)
                        raise ValueError("OCR 返回格式无效")
                except Exception as e:
                    st.error(f"OCR 请求失败: {e}")
                    st.stop()

                # Save files temporarily
                temp_excel_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
                temp_mpn_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
                temp_json_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name

                with open(temp_excel_path, "wb") as f:
                    f.write(uploaded_excel.read())
                with open(temp_mpn_path, "wb") as f:
                    f.write(uploaded_mpn_code.read())
                with open(temp_json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)

                # Call your function
                df = map_mpn_to_ocr_price(
                    temp_excel_path,
                    temp_mpn_path,
                    temp_json_path
                )

                st.success("✅ 填写完成！请查看或下载结果：")
                # st.balloons
                st.dataframe(df)

                from io import BytesIO
                buffer = BytesIO()
                df.to_excel(buffer, index=False)
                buffer.seek(0)

                st.download_button(
                    label="📥 下载Excel",
                    data=buffer,
                    file_name="mac_prices_filled.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.info("请上传所有3个文件以继续。")
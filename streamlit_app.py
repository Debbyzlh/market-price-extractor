import streamlit as st
import pandas as pd
import base64
import json
from io import BytesIO
from get_json import get_access_token, ocr_image_to_json
from json_to_tbl import extract_triplets_by_code_width

# Use your API credentials
YOUR_API_KEY = "Xkk7U2sOfAwEKT3BrH4Atucg"
YOUR_SECRET_KEY = "ss2Ki6UWcfuCM58spfKt22hhg8u91WIa"

st.set_page_config(layout="wide", page_title="Market Scanner")

# App UI
st.title("💻📱 市场价格抓取")

tabs = st.tabs(["iPhone", "iPad", "Mac"])

# Placeholder tabs
for tab in tabs[:2]:
    with tab:
        st.info("敬请期待！")

# ---- Mac Tab Implementation ----
with tabs[2]:
    st.header("上传Mac市场价格图片")

    uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png", "pdf"])
    if uploaded_file:
        st.image(uploaded_file, caption="上传的图片", use_container_width=True)

        if st.button("📤 提取数据"):
            with st.spinner("从百度获取OCR结果..."):
                image_bytes = uploaded_file.read()
                token = get_access_token(YOUR_API_KEY, YOUR_SECRET_KEY)
                json_data = ocr_image_to_json(image_bytes, token)

            st.success("OCR完成，提取表格中...")

            # Convert JSON to table
            records = extract_triplets_by_code_width(json_data["words_result"])
            df = pd.DataFrame(records)

            if df.empty:
                st.warning("没有提取到有效数据。")
            else:
                st.dataframe(df)

                # Download button
                buffer = BytesIO()
                df.to_excel(buffer, index=False)
                buffer.seek(0)

                st.download_button(
                    label="📥 下载Excel",
                    data=buffer,
                    file_name="mac_products.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
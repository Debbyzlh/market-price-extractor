import streamlit as st
import pandas as pd
import base64
import json
from io import BytesIO
from get_json import get_access_token, ocr_image_to_json, is_valid_image
from excel_code_price import map_mpn_to_ocr_price

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
    st.header("📷 图片 + Excel 自动映射")

    uploaded_img = st.file_uploader("上传Mac价格截图", type=["jpg", "jpeg", "png", "pdf"])   

    uploaded_excel = st.file_uploader("上带有CPU sheet 的Excel文件（文件名必须全英文）", type=["xlsx"])
    uploaded_mpn_code = st.file_uploader("上传 MPN-code 映射表", type=["xlsx"])

    if uploaded_img and uploaded_excel and uploaded_mpn_code:
        if st.button("📤 识别 + 映射"):
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

                st.success("✅ 映射完成！请查看或下载结果：")
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
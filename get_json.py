import base64
import requests
import json

# Replace with your actual Baidu API credentials
API_KEY = "Xkk7U2sOfAwEKT3BrH4Atucg"
SECRET_KEY = "ss2Ki6UWcfuCM58spfKt22hhg8u91WIa"

def get_access_token(api_key, secret_key):
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")


def ocr_image_to_json(image_bytes, access_token):
    import requests
    import base64
    import urllib.parse
    import streamlit as st

    if not access_token:
        return {"error": "missing access token"}
    # st.write(access_token)

    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token={access_token}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Encode image correctly: base64 -> URL encoded
    img_base64 = base64.b64encode(image_bytes).decode()
    # img_encoded = urllib.parse.quote_plus(img_base64)

    # data = {"image": img_encoded}
    data = {"image": img_base64}
    response = requests.post(url, headers=headers, data=data)

    #change
    # import streamlit as st
    # st.write(response.json())
    try:
        return response.json()
    except Exception:
        return {"error": "response not JSON", "raw": response.text}

# def extract_table(image_path):
#     access_token = get_access_token(API_KEY, SECRET_KEY)
#     if not access_token:
#         raise ValueError("❌ Failed to get access token")

#     url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token={access_token}"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}

#     with open(image_path, "rb") as f:
#         img_base64 = base64.b64encode(f.read()).decode()

#     payload = {"image": img_base64}
#     response = requests.post(url, data=payload, headers=headers)
#     data = response.json()

#     # Save to JSON
#     with open("baidu_body_cells-test04.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)

#     print("✅ Saved response to baidu_body_cells-test03.json")



def is_valid_image(image_bytes):
    from PIL import Image
    import io 
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()  # Will raise if corrupted or invalid
        return True
    except Exception as e:
        return False


# if __name__ == "__main__":
#     extract_table("/Users/lehanzhao/Desktop/抓/data/test03.jpg")  # replace with your image path
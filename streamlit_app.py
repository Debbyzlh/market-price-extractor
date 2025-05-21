import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Photo Upload Demo",
    layout="wide"
)

# Add a title
st.title("Market Price Reader")

# Create two columns for the upload blocks
col1, col2 = st.columns(2)

# First upload block
with col1:
    st.header("iPhone & iPad Photo Upload")
    # st.write("Upload your first photo here")
    photo1 = st.file_uploader(
        "Choose your first photo",
        type=["jpg", "jpeg", "png"],
        key="uploader1"
    )
    
    if photo1 is not None:
        st.image(photo1, caption="iPhone & iPad uploaded photo", use_column_width=True)
        st.write(f"Filename: {photo1.name}")
        st.write(f"File size: {photo1.size} bytes")

# Second upload block
with col2:
    st.header("Mac Photo Upload")
    # st.write("Upload your second photo here")
    photo2 = st.file_uploader(
        "Choose your second photo",
        type=["jpg", "jpeg", "png"],
        key="uploader2"
    )
    
    if photo2 is not None:
        st.image(photo2, caption="Mac uploaded photo", use_column_width=True)
        st.write(f"Filename: {photo2.name}")
        st.write(f"File size: {photo2.size} bytes") 


import pandas as pd
from io import BytesIO

# Add a separator
st.markdown("---")

# Excel Download Section
st.header("Excel Download Section")
st.write("Generate and download a sample Excel file")

# Create sample data
data = {
    'Product': ['iPhone', 'iPad', 'Mac'],
    'Price': [100, 200, 300],
    'Date': ['2025-01-01', '2025-01-02', '2025-01-03']
}
df = pd.DataFrame(data)

# Create a button to download the Excel file
def convert_df_to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)  # Reset pointer to beginning of file
    return output.getvalue()

excel_file = convert_df_to_excel()

st.download_button(
    label="Download Excel File",
    data=excel_file,
    file_name="sample_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Display the data as a preview
st.subheader("Preview of Market Price Data")
st.dataframe(df)
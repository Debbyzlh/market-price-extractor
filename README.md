# Market Price Reader

A Streamlit application for uploading and comparing photos from different devices (iPhone, iPad, and Mac) and generating Excel reports.

## Features

- Upload and preview photos from different devices
- Display file information (filename and size)
- Generate and download sample Excel files with market price data
- Preview market price data in a table format

## Setup

1. Install the required packages:
```bash
pip3 install streamlit pandas xlsxwriter
```

2. Run the application:
```bash
streamlit run streamlit_app.py
```

## Usage

1. Use the file uploaders to upload photos from your devices
2. View the uploaded photos and their information
3. Generate and download sample Excel files using the "Download Excel File" button
4. Preview the market price data in the table below

## Requirements

- Python 3.x
- Streamlit
- Pandas
- XlsxWriter 
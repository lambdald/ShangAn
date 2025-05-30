"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:25:36
LastEditors: lidong lambdald@outlook.com
LastEditTime: 2025-05-29 11:36:38
Description: 
"""
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend
from pathlib import Path
st.set_page_config(layout="wide")


data_dir = Path(r"data")
assert data_dir.exists(), f"Data directory {data_dir} does not exist."

shengkao_dir = data_dir / "ShengKao"
assert shengkao_dir.exists(), f"ShengKao directory {shengkao_dir} does not exist."

provinces = sorted(shengkao_dir.iterdir())
selected_province = st.selectbox("Select a province", provinces)

if selected_province:
    selected_province_dir = shengkao_dir / selected_province.name
    assert selected_province_dir.exists(), f"Selected province directory {selected_province_dir} does not exist."

file_path = selected_province_dir / "data.parquet"
assert file_path.exists(), f"File {file_path} does not exist."



@st.cache_data
def get_tesla_data():
    df = pd.read_parquet(file_path)
    return df

tesla_data = get_tesla_data()

new_dfs, code = spreadsheet(tesla_data)
code = code if code else "# Edit the spreadsheet above to generate code"
st.code(code)

def clear_mito_backend_cache():
    _get_mito_backend.clear()

# Function to cache the last execution time - so we can clear periodically
@st.cache_resource
def get_cached_time():
    # Initialize with a dictionary to store the last execution time
    return {"last_executed_time": None}

def try_clear_cache():

    # How often to clear the cache
    CLEAR_DELTA = timedelta(hours=12)

    current_time = datetime.now()
    cached_time = get_cached_time()

    # Check if the current time is different from the cached last execution time
    if cached_time["last_executed_time"] is None or cached_time["last_executed_time"] + CLEAR_DELTA < current_time:
        clear_mito_backend_cache()
        cached_time["last_executed_time"] = current_time

try_clear_cache()
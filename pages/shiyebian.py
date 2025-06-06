"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:25:36
LastEditors: Lambdald lambdald@163.com
LastEditTime: 2025-05-29 22:50:35
Description: 
"""
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend
from shangan.dataparser.xls_parser import XLSParser

# 实例化XLSParser类
parser = XLSParser()

# 解析xls文件
file_path = r'data\ShiYeDanWei\ShanXi\职位表.xls'

st.set_page_config(layout="wide")

@st.cache_data
def get_tesla_data():
    df = parser.parse_xls(file_path)
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
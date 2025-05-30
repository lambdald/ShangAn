"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:35:52
LastEditors: lidong lambdald@outlook.com
LastEditTime: 2025-05-29 13:51:23
Description: 
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import ast
# 实例化XLSParser类
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

linechart_columns = [
    '提交报名申请',
    '审查通过人数',
    '缴费人数'
]

df = pd.read_parquet(file_path)

max_val_s = df[linechart_columns].max()
print(max_val_s)
max_vals = {}
for k in linechart_columns:
    max_vals[k] = max_val_s[k].max()
print(max_vals)

st.dataframe(
    df,
    column_config={
        k: st.column_config.LineChartColumn(k, y_min=0, y_max=max_vals[k]) for k in linechart_columns
    },
    hide_index=True,
)
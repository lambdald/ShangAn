"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:35:52
LastEditors: lidong lambdald@outlook.com
LastEditTime: 2025-05-30 15:01:43
Description: 
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import ast
# 实例化XLSParser类
st.set_page_config(layout="wide")
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)

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

# df.drop(columns=["JobID"], inplace=True)
# for col in df.columns:
#     print(col)
#     if df[col].dtype in [np.int64, np.int32]:
#         df[col] = df[col].map(str)
#     print('column type: ', df[col].dtype)

max_val_s = df[linechart_columns].map(max)


# df[linechart_columns] = df[linechart_columns].map(str)
# print(type(df[linechart_columns].iloc[0,0]))
print(max_val_s)
max_vals = {}
for k in linechart_columns:
    max_vals[k] = int(max_val_s[k].max())
print(max_vals)

filters = {}

for column in df.columns:
    if column in linechart_columns:
        continue
    if is_string_dtype(df[column]):
        col1, col2 = st.columns(2)
        filters[column] =  [
            col1.text_input(f"Filter for {column}", key=column),
            col2.button("Apply", key=f"apply_{column}")
        ]

df_show = df.copy()
for column in df.columns:
    if column in linechart_columns or column not in filters:
        continue
    if filters[column][1]:
        df_show = df_show[df_show[column].str.contains(filters[column][0])]

st.dataframe(
    df_show,
    column_config={
        k: st.column_config.LineChartColumn(k, y_min=0, y_max=2000) for k in linechart_columns
    },
    hide_index=True,
)
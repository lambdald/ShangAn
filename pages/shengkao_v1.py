"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:35:52
LastEditors: Lambdald lambdald@163.com
LastEditTime: 2025-05-28 22:37:29
Description: 
"""
import streamlit as st
import pandas as pd
import numpy as np
from shangan.dataparser.xls_parser import XLSParser

# 实例化XLSParser类
parser = XLSParser()

# 解析xls文件
file_path = r'data\ShengKao\ShanXi\职位表.xls'
df = parser.parse_xls(file_path)
st.dataframe(df)  # Same as st.write(df)
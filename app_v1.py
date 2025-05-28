"""
Author: Lambdald lambdald@163.com
Date: 2025-05-28 22:35:52
LastEditors: Lambdald lambdald@163.com
LastEditTime: 2025-05-28 22:36:00
Description: 
"""
import streamlit as st
import pandas as pd
import numpy as np
df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))
st.dataframe(df)  # Same as st.write(df)
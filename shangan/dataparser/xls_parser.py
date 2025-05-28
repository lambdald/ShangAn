"""
Author: lidong lambdald@outlook.com
Date: 2025-05-27 17:52:08
LastEditors: lidong lambdald@outlook.com
LastEditTime: 2025-05-28 09:51:10
Description: 读取xls文件，并解析
"""

import xlrd
from pathlib import Path
import pandas as pd
from typing import List, Dict


def read_xls(file_path: str | Path) -> Dict[str, pd.DataFrame]:
    """
    读取xls文件，返回sheet的名称和内容
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    
    if not file_path.suffix.lower() in ['.xls', '.xlsx']:
        raise ValueError(f"File {file_path} is not a xls or xlsx file")

    workbook = xlrd.open_workbook(file_path)
    if workbook.nsheets == 0:
        raise ValueError(f"File {file_path} has no sheet")
    sheets = {}
    for sheet_index in range(workbook.nsheets):
        sheet_name = workbook.sheet_names()[sheet_index]
        data = pd.read_excel(file_path, sheet_name=sheet_index)
        data.columns = data.loc[0]
        data = data.drop(index=[0]).reset_index(drop=True)
        data.insert(0, '系统', sheet_name)  # 在第一列插入系统名称
        sheets[sheet_name] = data
    return sheets



class XLSParser:
    def __init__(self):
        pass

    def parse_xls(self, file_path: str | Path) -> List[Dict[str, str]]:
        """
        解析xls文件，返回sheet的名称和内容
        """
        file_path = Path(file_path)

if __name__ == "__main__":
    file_path = r'data\ShengKao\ShanXi\职位表.xls'
    sheets = read_xls(file_path)
    for sheet_name, df in sheets.items():
        print(f"Sheet: {sheet_name}")
        print(df.columns.tolist())
        print(df.loc[0].tolist())
        # print(df.)
        print("\n")

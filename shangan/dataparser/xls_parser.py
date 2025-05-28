"""
Author: lidong lambdald@outlook.com
Date: 2025-05-27 17:52:08
LastEditors: Lambdald lambdald@163.com
LastEditTime: 2025-05-28 23:10:05
Description: 读取xls文件，并解析
"""

import xlrd
from pathlib import Path
import pandas as pd
from typing import List, Dict


def read_xls(file_path: str | Path) -> pd.DataFrame:
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
    
    if workbook.nsheets == 1:
        data = pd.read_excel(file_path)
        data.columns = data.loc[0]
        data = data.drop(index=[0]).reset_index(drop=True)
        return data
    sheets = {}
    for sheet_index in range(workbook.nsheets):
        sheet_name = workbook.sheet_names()[sheet_index]
        data = pd.read_excel(file_path, sheet_name=sheet_index)
        data.columns = data.loc[0]
        data = data.drop(index=[0]).reset_index(drop=True)
        data.insert(0, '系统', sheet_name)  # 在第一列插入系统名称
        sheets[sheet_name] = data

    # 检查是否有重复的列名
    all_data = pd.concat(sheets.values(), ignore_index=True)
    return all_data



class XLSParser:
    def __init__(self):
        pass

    def parse_xls(self, file_path: str | Path) -> pd.DataFrame:
        """
        解析xls文件，返回sheet的名称和内容
        """
        file_path = Path(file_path)
        df = read_xls(file_path)
        return df

class ShengKaoParser(XLSParser):
    def __init__(self):
        super().__init__()

    def parse_zhiweibiao(self, file_path: str | Path) -> pd.DataFrame:
        """
        解析职位表.xls文件，返回职位表的内容
        """
        file_path = Path(file_path)
        df = read_xls(file_path)
        df.insert(0, 'JobID', range(1, len(df) + 1))
        return df
    
    def parse_baomingqingkuang(self, file_path: List[Path]) -> List[pd.DataFrame]:
        result = {}
        for file in file_path:
            df = read_xls(file)
            info = df['招录单位'].str.split('-', expand=True)
            info.columns = ['系统','招录部门', '招录单位']

            df.drop(columns=['招录单位'], inplace=True)
            df = pd.concat([info, df], axis=1)
            date = file.stem.split('-')[1]
            result[date] = df
        return result
    
    def merge(self, zhiweibiao: pd.DataFrame, baomingqingkuang: List[pd.DataFrame]) -> pd.DataFrame:
        """
        合并报名情况表
        """
        job_stat = {}
        for date, df in baomingqingkuang.items():
            stat = zhiweibiao.merge(df, on=['招录部门', '招录单位', '招录职位', '招录人数'], how='left')
            print(stat.columns)
            print(stat.head(2))
            
            


if __name__ == "__main__":
    file_path = r'data\ShengKao\ShanXi\职位表.xls'
    df = read_xls(file_path)
    print(df.columns)
    print(df.head(2))

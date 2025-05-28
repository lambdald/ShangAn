"""
Author: lidong lambdald@outlook.com
Date: 2025-05-28 09:28:47
LastEditors: lidong lambdald@outlook.com
LastEditTime: 2025-05-28 09:28:54
Description: 
"""
import pandas as pd
import duckdb as db
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = PROJECT_DIR / 'data' / 'shangan.csv'
from typing import List, Dict, Any, Union

class DataEngine:
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = db_path
        self.conn = db.connect(str(db_path))
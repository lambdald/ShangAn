from pathlib import Path
import pandas as pd
import streamlit as st
from shangan.dataparser.xls_parser import ShengKaoShanXiParser


def main():
    data_dir = Path(r"data")
    assert data_dir.exists(), f"Data directory {data_dir} does not exist."
    for job_dir in sorted(data_dir.iterdir()):
        if not job_dir.is_dir():
            continue

        for province_dir in sorted(job_dir.iterdir()):
            if not province_dir.is_dir():
                continue

            zhiweibiao = province_dir / "职位表.xls"
            baomingqingkuang = sorted(province_dir.glob("报名情况*.xls"))
            if not zhiweibiao.exists() or not baomingqingkuang:
                continue

            parser = ShengKaoShanXiParser()
            zhiweibiao_df = parser.parse_zhiweibiao(zhiweibiao)
            baomingqingkuang_df = parser.parse_baomingqingkuang(baomingqingkuang)
            final_data = parser.merge(zhiweibiao_df, baomingqingkuang_df)

            final_data.to_parquet(province_dir / "data.parquet", index=False)
            print(f"Processing {zhiweibiao} and {baomingqingkuang}")

if __name__ == "__main__":
    main()

# utils.py
import pandas as pd
import zipfile
from pathlib import Path

def load_esg_zip(zip_path: str | Path = "esg_cleaned_final.csv.zip") -> pd.DataFrame:
    """
    Robustly load the first CSV found inside a ZIP archive.
    """
    zip_path = Path(zip_path)
    if not zip_path.exists():
        raise FileNotFoundError(f"{zip_path} not found")

    with zipfile.ZipFile(zip_path) as zf:
        # 找到第一个 .csv 文件；如果你知道确切名字可直接写
        csv_files = [name for name in zf.namelist() if name.lower().endswith("esg_cleaned_final.csv")]
        if not csv_files:
            raise ValueError("No CSV found inside the ZIP archive")
        with zf.open(csv_files[0]) as fp:
            return pd.read_csv(fp)

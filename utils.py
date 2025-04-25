# utils.py
import pandas as pd
from pathlib import Path
import zipfile

def load_esg_zip(path: str | Path = "esg_cleaned_final.csv.zip") -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            csv_files = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            with zf.open(csv_files[0]) as fp:
                return pd.read_csv(fp)

    # 回退：普通 CSV
    return pd.read_csv(path)

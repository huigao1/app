# utils.py
import pandas as pd
import zipfile
from pathlib import Path

def load_esg_zip(
    zip_path: str | Path = "esg_cleaned_final.csv.zip",
    csv_name: str = "esg_cleaned_final.csv"
) -> pd.DataFrame:
    """
    Robustly load a CSV inside a ZIP archive.

    Parameters
    ----------
    zip_path : str or Path
        Path to the .zip file (relative to repo root by default)
    csv_name : str
        CSV file name inside the zip

    Returns
    -------
    pandas.DataFrame
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file '{zip_path}' not found.")

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            if csv_name not in zip_ref.namelist():
                raise FileNotFoundError(
                    f"CSV file '{csv_name}' not found inside '{zip_path.name}'. "
                    f"Files available: {zip_ref.namelist()}"
                )

            with zip_ref.open(csv_name) as csv_file:
                return pd.read_csv(csv_file)

    except zipfile.BadZipFile as e:
        raise zipfile.BadZipFile(f"Invalid zip file '{zip_path}'.") from e

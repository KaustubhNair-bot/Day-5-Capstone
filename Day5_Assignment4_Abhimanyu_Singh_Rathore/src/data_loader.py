# src/data_loader.py

import pandas as pd

class DataLoadError(Exception):
    pass


def load_city_data(csv_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise DataLoadError(f"CSV file not found at path: {csv_path}")
    except Exception as e:
        raise DataLoadError(f"Failed to load CSV: {str(e)}")

    required_columns = {"city", "country", "lat", "lng", "population"}
    missing = required_columns - set(df.columns)

    if missing:
        raise DataLoadError(f"Missing required columns: {missing}")

    return df[list(required_columns)]

import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names: lowercase and replace spaces with underscores.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def clean_city_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize city names for consistent merging.
    """
    df["city"] = (
        df["city"]
        .str.strip()
        .str.lower()
    )
    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing critical values.
    """
    df = df.dropna(subset=["city", "lat", "lng"])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate city entries.
    """
    df = df.drop_duplicates(subset=["city"])
    return df


def clean_city_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all cleaning steps in correct order.
    """
    df = normalize_column_names(df)
    df = clean_city_names(df)
    df = remove_invalid_rows(df)
    df = remove_duplicates(df)

    return df

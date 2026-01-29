import pandas as pd
import pytest
from src.data_cleaner import DataCleaner


def test_clean_removes_duplicates():
    cleaner = DataCleaner()
    # Create dummy data with a duplicate city
    data = {
        "city": ["Jaipur", "Jaipur", "Tokyo"],
        "country": ["India", "India", "Japan"],
        "lat": [26.9, 26.9, 35.6],
        "lng": [75.7, 75.7, 139.6],
        "population": [3000000, 3000000, 14000000],
    }
    df = pd.DataFrame(data)

    cleaned_df = cleaner.clean(df)

    # Assert that the duplicate Jaipur was removed
    assert len(cleaned_df) == 2
    # Assert casing was standardized to lowercase
    assert "jaipur" in cleaned_df["city"].values


def test_clean_drops_nulls():
    cleaner = DataCleaner()
    # Create dummy data with a missing population
    data = {
        "city": ["Jaipur", "Delhi"],
        "country": ["India", "India"],
        "lat": [26.9, 28.6],
        "lng": [75.7, 77.2],
        "population": [3000000, None],  # Delhi has no population
    }
    df = pd.DataFrame(data)

    cleaned_df = cleaner.clean(df)

    # Assert that Delhi was dropped
    assert len(cleaned_df) == 1
    assert "delhi" not in cleaned_df["city"].values

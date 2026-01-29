import pandas as pd
from src.data_cleaner import clean_city_data


def test_remove_null_lat_lng():
    df = pd.DataFrame({
        "city": ["Mumbai", "Delhi"],
        "lat": [19.07, None],
        "lng": [72.87, 77.21]
    })

    cleaned_df = clean_city_data(df)

    assert len(cleaned_df) == 1
    assert cleaned_df.iloc[0]["city"] == "mumbai"


def test_remove_duplicate_cities():
    df = pd.DataFrame({
        "city": ["Mumbai", "Mumbai"],
        "lat": [19.07, 19.07],
        "lng": [72.87, 72.87]
    })

    cleaned_df = clean_city_data(df)

    assert len(cleaned_df) == 1

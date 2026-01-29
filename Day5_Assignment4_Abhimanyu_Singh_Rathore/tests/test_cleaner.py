import pandas as pd
from src.data_cleaner import clean_city_data

def test_clean_city_data_removes_nulls_and_duplicates():
    # Arrange: fake input data
    data = {
        "city": ["Delhi", "Delhi", None],
        "country": ["India", "India", "India"],
        "lat": [28.61, 28.61, 28.61],
        "lng": [77.21, 77.21, 77.21],
        "population": [30000000, 30000000, None]
    }

    df = pd.DataFrame(data)

    # Act: clean the data
    cleaned_df = clean_city_data(df)

    # Assert: only one valid row remains
    assert len(cleaned_df) == 1
    assert cleaned_df.iloc[0]["city"] == "delhi"

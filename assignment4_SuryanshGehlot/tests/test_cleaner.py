# removes nulls and removes duplicates from city table

import pandas as pd
from src.data_cleaner import clean_city_table

def test_removes_null_coordinates():

    raw = pd.DataFrame({
        "city" : ["Delhi","Jaipur","Washington"],
        "country" : ["India","India","USA"],
        "lat" : [28.61, None, 38.90],
        "lng" : [77.23, 75.79, None],
        "population" : [19000000, 3000000, 7000000]
    })

    cleaned = clean_city_table(raw) #clean the raw data

    assert len(cleaned) == 1 #only Delhi remains
    assert cleaned.iloc[0]["city"] == "delhi" ##iloc is for integer-location based indexing for selection by position ;city name is lowercased

def test_removes_duplicates():
    raw = pd.DataFrame({
        "city" : ["Delhi","delhi","Jaipur"],
        "country" : ["India","India","India"],
        "lat" : [28.61, 28.61, 26.91],
        "lng" : [77.23, 77.23, 75.79],
        "population" : [19000000, 19000000, 3000000]
    })

    cleaned = clean_city_table(raw)

    assert len(cleaned) == 2
    assert "delhi" in cleaned["city"].values
    assert "jaipur" in cleaned["city"].values

#assert is the heart of unit testing
#if true test passes else fails immediately n raises an AssertionError
#cleaned["city"].values → array of city names

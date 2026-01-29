import sys
import os
import pytest
import pandas as pd

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import clean_city_data


def test_clean_city_data_handle_null_values():
    # Create a DataFrame with some null values in crucial columns
    data = pd.DataFrame({
        "city": ["New York", "Los Angeles", None, "Chicago"],
        "country": ["USA", "USA", "USA", "USA"],
        "lat": [40.7128, 34.0522, None, 41.8781],
        "lng": [-74.0060, -118.2437, None, -87.6298],
        "population": [8000000, 4000000, 2000000, 2700000]
    })
    
    # Clean the data using the function
    cleaned_data = clean_city_data(data)
    
    # After cleaning, the row with a missing 'city' should be removed
    assert cleaned_data.shape[0] == 3  # There should be 3 rows remaining
    assert cleaned_data['city'].isnull().sum() == 0  # No null values in 'city' column

def test_clean_city_data_remove_duplicates():
    # Create a DataFrame with duplicate city-country entries
    data = pd.DataFrame({
        "city": ["New York", "Los Angeles", "New York", "Chicago"],
        "country": ["USA", "USA", "USA", "USA"],
        "lat": [40.7128, 34.0522, 40.7128, 41.8781],
        "lng": [-74.0060, -118.2437, -74.0060, -87.6298],
        "population": [8000000, 4000000, 8000000, 2700000]
    })
    

    # Clean the data using the function
    cleaned_data = clean_city_data(data)
    
    # After cleaning, there should be only one row for "New York"
    assert cleaned_data.shape[0] == 3  # One duplicate row of New York should be removed
    assert cleaned_data["city"].value_counts()["new york"] == 1  # Only one entry for New York

def test_clean_city_data_normalize_columns():
    # Create a DataFrame with irregular column names
    data = pd.DataFrame({
        "City ": ["New York", "Los Angeles", "Chicago"],
        "Country ": ["USA", "USA", "USA"],
        "Lat ": [40.7128, 34.0522, 41.8781],
        "Lng ": [-74.0060, -118.2437, -87.6298],
        "Population ": [8000000, 4000000, 2700000]
    })
    
    # Clean the data using the function
    cleaned_data = clean_city_data(data)
    
    # After cleaning, the column names should be normalized (stripped and lowercased)
    assert "city" in cleaned_data.columns  # 'City' should become 'city'
    assert "country" in cleaned_data.columns  # 'Country' should become 'country'
    assert "lat" in cleaned_data.columns  # 'Lat' should become 'lat'
    assert "lng" in cleaned_data.columns  # 'Lng' should become 'lng'
    assert "population" in cleaned_data.columns  # 'Population' should become 'population'
    
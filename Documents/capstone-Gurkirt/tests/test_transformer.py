import pytest
import pandas as pd
from src import transform_weather_data
from unittest.mock import patch

# Mocking the 'transform_weather_data' function to avoid external API calls
@patch("src.transformer.transform_weather_data")
def test_transform_weather_data(mock_transform_weather_data):
    # Mocking the API call to return a fixed response for weather data
    mock_transform_weather_data.return_value = {
        "main": {"temp": 20, "humidity": 80},
        "weather": [{"main": "Clear"}]
    }

    # Create a small sample DataFrame representing cleaned city data
    city_data = pd.DataFrame({
        "city": ["New York", "Los Angeles", "Chicago"],
        "country": ["USA", "USA", "USA"],
        "lat": [40.7128, 34.0522, 41.8781],
        "lng": [-74.0060, -118.2437, -87.6298],
        "population": [8000000, 4000000, 2700000]
    })

    # Transform the data
    transformed_data = transform_weather_data()

    # Ensure the transformed data is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)
    
    # Ensure the 'temperature_category' column exists
    assert "temperature_category" in transformed_data.columns

    # Ensure the 'population_bucket' column exists
    assert "population_bucket" in transformed_data.columns

def test_temperature_category_logic():
    # Create sample data for testing temperature categories
    data = pd.DataFrame({
        "city": ["City A", "City B", "City C"],
        "temperature": [10, 25, 30]
    })
    # Categorize temperature manually (Cold, Moderate, Hot)
    data['temperature_category'] = data['temperature'].apply(
        lambda temp: 'Cold' if temp < 15 else ('Moderate' if temp <= 25 else 'Hot')
    )

    # Test if the categorization is correct
    assert data['temperature_category'].iloc[0] == 'Cold'
    assert data['temperature_category'].iloc[1] == 'Moderate'
    assert data['temperature_category'].iloc[2] == 'Hot'

def test_population_bucket():
    # Create sample data for testing population buckets
    data = pd.DataFrame({
        "city": ["City A", "City B", "City C"],
        "population": [8000000, 4000000, 12000000]
    })

    # Define population bins and labels for testing
    bins = [0, 1_000_000, 5_000_000, 10_000_000, float('inf')]
    labels = ['0M-1M', '1M-5M', '5M-10M', '10M+']
    data['population_bucket'] = pd.cut(data['population'], bins=bins, labels=labels, right=False)

    # Test if the population bucket categorization is correct
    assert data['population_bucket'].iloc[0] == '5M-10M'
    assert data['population_bucket'].iloc[1] == '1M-5M'
    assert data['population_bucket'].iloc[2] == '10M+'
import pytest
from src.transformer import DataProcessor


def test_temperature_categorization():
    processor = DataProcessor()

    # Test cases for the business logic
    assert processor.get_temp_category(10) == "Cold"
    assert processor.get_temp_category(20) == "Moderate"
    assert processor.get_temp_category(30) == "Hot"


def test_population_bucketing():
    processor = DataProcessor()

    # Test cases for population logic
    assert processor.get_pop_bucket(500000) == "Small"
    assert processor.get_pop_bucket(5000000) == "Medium"
    assert processor.get_pop_bucket(15000000) == "Large"

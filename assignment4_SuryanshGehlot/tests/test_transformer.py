# tests validate feature-engineering logic in transformer.py

import pandas as pd
from src.transformer import transform_city_data


def test_temperature_category_ranges():
    sample = pd.DataFrame({
        "temp": [-5, 5, 15, 25, 35],
        "population": [1_000_000] * 5
    })

    result = transform_city_data(sample)

    assert result["temp_category"].tolist() == [
        "Freezing",
        "Cold",
        "Mild",
        "Warm",
        "Hot"
    ]


def test_population_bucket_ranges():
    sample = pd.DataFrame({
        "temp": [20, 20, 20, 20],
        "population": [
            500_000,
            2_000_000,
            7_000_000,
            20_000_000
        ]
    })

    result = transform_city_data(sample)

    assert result["population_bucket"].tolist() == [
        "Small",
        "Medium",
        "Large",
        "Mega"
    ]

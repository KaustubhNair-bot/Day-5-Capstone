from src.transformer import temperature_category, population_bucket


def test_temperature_category():
    assert temperature_category(10) == "Cold"
    assert temperature_category(20) == "Moderate"
    assert temperature_category(35) == "Hot"


def test_population_bucket():
    assert population_bucket(2_000_000) == "Medium"
    assert population_bucket(15_000_000) == "Large"

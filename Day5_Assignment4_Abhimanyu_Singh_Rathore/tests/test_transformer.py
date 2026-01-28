# import the function to test
from src.transformer import temperature_category


# test checks the "Cold" condition.
# Give a temperature value (10°C),
# which is clearly below the cold threshold.
# If the function works correctly, it should return "Cold".
def test_temperature_category_cold():
    assert temperature_category(10) == "Cold"


# test checks the "Moderate" temperature range.
# 25°C lies between the cold and hot limits.
def test_temperature_category_moderate():
    assert temperature_category(25) == "Moderate"


# test checks the "Hot" condition.
# 40°C is above the hot threshold.
def test_temperature_category_hot():
    assert temperature_category(40) == "Hot"

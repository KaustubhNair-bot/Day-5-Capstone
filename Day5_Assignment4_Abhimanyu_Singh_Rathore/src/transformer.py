

import pandas as pd
from src.api_client import fetch_weather, WeatherAPIError


def temperature_category(temp: float) -> str:
    """
    Categorizes a temperature value into a human-readable bucket.

    rules:
    - Below 20°C  → Cold
    - 20°C–35°C   → Moderate
    - Above 35°C  → Hot
    """
    if temp < 20:
        return "Cold"
    elif temp <= 35:
        return "Moderate"
    return "Hot"


def enrich_with_weather(df: pd.DataFrame, api_key: str) -> pd.DataFrame:
    """
    For each city:
    - Calls the weather API using latitude & longitude
    - Extracts temperature, humidity, and weather condition
    - Derives a temperature category (Cold / Moderate / Hot)

    Parameters:
        df (pd.DataFrame): Cleaned city data
        api_key (str): OpenWeather API key

    Returns:
        pd.DataFrame: DataFrame enriched with weather information
    """

 
    temperatures = []
    humidities = []
    conditions = []

    # Iterate over each city row.
    for _, row in df.iterrows():
        try:
            # Fetch weather data for the city using coordinates.
            # Lat/Lng are used because city names can be ambiguous.
            weather = fetch_weather(row["lat"], row["lng"], api_key)

        except WeatherAPIError as e:
            raise RuntimeError(
                f"Weather fetch failed for city {row['city']}: {e}"
            )

        # Collect weather attributes for this city.
        temperatures.append(weather["temperature"])
        humidities.append(weather["humidity"])
        conditions.append(weather["weather_condition"])

    # add the new columns to the DataFrame in one step.
    df["temperature"] = temperatures
    df["humidity"] = humidities
    df["weather_condition"] = conditions

    # Apply the temperature_category function to each temperature
    # to derive a new feature used by API filters.
    df["temp_category"] = df["temperature"].apply(temperature_category)

    # Return the enriched DataFrame to be served via APIs
    return df

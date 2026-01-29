import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("OPENWEATHER_API_KEY")

print("loaded api key:", api_key)

def fetch_weather_data(city_name, api_key):
    """Fetch weather data for a given city from the OpenWeatherMap API."""

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code} for {city_name}")

    data=response.json()

    with open(f"data/raw/{city_name}_weather.json", "w") as f:
        json.dump(data, f, indent=4)

    return data

if __name__ == "__main__":
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    for city in cities:
        weather_data = fetch_weather_data(city, api_key)
        if weather_data:
            desc = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            print(f"{city}: {desc}, {temp}°C")

# src/api_client.py

import requests

class WeatherAPIError(Exception):
    pass


def fetch_weather(lat: float, lng: float, api_key: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lng,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Network error while calling Weather API: {e}")

    if response.status_code != 200:
        raise WeatherAPIError(
            f"Weather API failed [{response.status_code}]: {response.text}"
        )

    try:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_condition": data["weather"][0]["main"]
        }
    except (KeyError, IndexError):
        raise WeatherAPIError("Unexpected Weather API response structure")

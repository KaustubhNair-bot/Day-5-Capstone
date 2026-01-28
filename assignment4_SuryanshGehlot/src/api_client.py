# calls an OpenWeather API and processes the response; handles errors appropriately; returns python data (dict)

import requests

def fetch_weather(city_name:str,api_key:str) ->dict:

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    try:

        response = requests.get(base_url, params=params, timeout=10)

        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        payload = response.json()

        return {
            "city": city_name.lower(),
            "temp": payload["main"]["temp"],
            "humidity": payload["main"]["humidity"],
            "condition": payload["weather"][0]["main"].lower()
        }

    except (requests.exceptions.RequestException, KeyError) as e:

        print(f"Error fetching weather data for {city_name}: {e}")

        return {
            "city": city_name.lower(),
            "temp": None,
            "humidity": None,
            "condition": None
        }
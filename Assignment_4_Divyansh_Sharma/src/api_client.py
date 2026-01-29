import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherAPI:
    # Handles fetching data from external OpenWeatherMap API.

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        # Directory to store raw API responses as per Task 87
        self.raw_responses_dir = "data/raw/responses"
        os.makedirs(self.raw_responses_dir, exist_ok=True)

    def fetch_weather_data(self, city_name):
        # Fetches real-time weather data for a specific city.
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(self.base_url, params=params)
            # Checking if the request was successful or not
            if response.status_code == 200:
                data = response.json()

                # Save raw API response as JSON
                json_path = os.path.join(
                    self.raw_responses_dir, f"{city_name.lower()}.json"
                )
                with open(json_path, "w") as f:
                    json.dump(data, f, indent=4)

                return {
                    "city": city_name,
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "weather_condition": data["weather"][0]["description"],
                }
            else:
                print(
                    f"Failed to fetch weather for {city_name}: {response.status_code}"
                )
                return None

        except Exception as e:
            print(f"An error occurred while calling the API: {e}")
            return None

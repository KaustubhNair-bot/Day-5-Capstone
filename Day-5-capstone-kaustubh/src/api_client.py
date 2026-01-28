import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

    def fetch_weather_by_city(self, city_name: str) -> dict:
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                f"API request failed for {city_name}: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    def save_raw_response(self, city_name: str, data: dict) -> None:
        os.makedirs("data/raw", exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"data/raw/weather_{city_name.lower()}_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

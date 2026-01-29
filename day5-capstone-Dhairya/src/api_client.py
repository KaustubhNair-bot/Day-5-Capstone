import requests
import json
from datetime import datetime
from pathlib import Path 
from logger import get_logger
import os 
from dotenv import load_dotenv

load_dotenv()

logger = get_logger("api_client")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("WEATHER_API")

def fetch_weather_data(latitude: float, longitude: float, city: str) -> dict:

    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in environment variables")
      
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature_celsius = round(data["main"]["temp"] - 273.15, 2)
        logger.info(f"Fetching weather for {city}")
        return {
            "city": city.lower(),
            "temperature": temperature_celsius,
            "weathercode": data["weather"][0]["description"],
            "windspeed": data["wind"]["speed"]
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather for {city}: {e}")
        return {}
    
def save_raw_weather_data(weather_data: list) -> None:
    """
    Save raw weather API response as JSON.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    output_dir = BASE_DIR / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"weather_raw_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(weather_data, f, indent=4)

    print(f"[INFO] Raw weather data saved at {file_path}")

def fetch_weather_for_cities(cities: list) -> list:
    """
    Fetch weather data for multiple cities.
    """
    all_weather_data = []

    for city in cities:
        weather = fetch_weather_data(
            latitude=city["lat"],
            longitude=city["lng"],
            city=city["city"]
        )
        if weather:
            all_weather_data.append(weather)

    save_raw_weather_data(all_weather_data)
    return all_weather_data

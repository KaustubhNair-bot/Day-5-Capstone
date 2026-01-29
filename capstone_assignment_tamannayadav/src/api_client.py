"""
API Client module for fetching weather data from Open-Meteo API.
"""
import requests
import json
import os
import logging

logger = logging.getLogger(__name__)


class WeatherAPIClient:
    """Client for fetching weather data from Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_weather(self, lat, lng, city_name):
        """
        Fetch weather data for a given latitude and longitude.
        
        Args:
            lat: Latitude of the city
            lng: Longitude of the city
            city_name: Name of the city
            
        Returns:
            dict: Weather data including temperature, humidity, and condition
        """
        params = {
            "latitude": lat,
            "longitude": lng,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "auto"
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            
            return {
                "city": city_name,
                "lat": lat,
                "lng": lng,
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "weather_code": current.get("weather_code"),
                "weather_condition": self._get_weather_condition(current.get("weather_code"))
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather for {city_name}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing response for {city_name}: {e}")
            return None
    
    def _get_weather_condition(self, code):
        """Convert WMO weather code to human-readable condition."""
        if code is None:
            return "Unknown"
        
        conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail"
        }
        return conditions.get(code, "Unknown")
    
    def fetch_weather_for_cities(self, cities_data):
        """
        Fetch weather data for multiple cities.
        
        Args:
            cities_data: List of dicts with city, lat, lng keys
            
        Returns:
            list: List of weather data dictionaries
        """
        weather_data = []
        
        for city in cities_data:
            result = self.fetch_weather(
                city["lat"],
                city["lng"],
                city["city"]
            )
            if result:
                weather_data.append(result)
        
        logger.info(f"Fetched weather for {len(weather_data)} cities")
        return weather_data
    
    def save_raw_response(self, data, filepath):
        """Save raw API response as JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved raw response to {filepath}")


if __name__ == "__main__":
    # Test the API client
    client = WeatherAPIClient()
    
    test_cities = [
        {"city": "Tokyo", "lat": 35.6870, "lng": 139.7495},
        {"city": "Delhi", "lat": 28.6100, "lng": 77.2300},
        {"city": "New York", "lat": 40.6943, "lng": -73.9249},
        {"city": "London", "lat": 51.5074, "lng": -0.1278},
        {"city": "Sydney", "lat": -33.8688, "lng": 151.2093}
    ]
    
    weather = client.fetch_weather_for_cities(test_cities)
    print(json.dumps(weather, indent=2))

# CSV loading, cleaning, calling Weather API, merging, and saving final CSV

import os
import pandas as pd
from dotenv import load_dotenv

from src.data_loader import load_city_table
from src.data_cleaner import clean_city_table
from src.api_client import fetch_weather
from src.transformer import transform_city_data

RAW_CSV_PATH = "data/raw/worldcities.csv"
OUTPUT_CSV_PATH = "data/processed/merged_data.csv"

def run_pipeline():

    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError("API key for OpenWeather is not set in environment variables.")
    
    city_table = load_city_table(RAW_CSV_PATH)

    cleaned_table = clean_city_table(city_table)

    selected_cities = cleaned_table.head(5)

    weather_rows = [] #list of dicts to hold merged data

    for _, row in selected_cities.iterrows(): #iterate over each city gives index and row; we use _ for index as we don't need it

        weather_info = fetch_weather(row["city"], api_key)

        weather_rows.append({
            "city": row["city"],
            "country": row["country"],
            "lat": row["lat"],
            "lng": row["lng"],
            "population": row["population"],
            "temp": weather_info["temp"],
            "humidity": weather_info["humidity"],
            "condition": weather_info["condition"]
        })
    
    merged_table = pd.DataFrame(weather_rows)

    final_table = transform_city_data(merged_table) #add derived columns

    os.makedirs("data/processed", exist_ok=True) #ensure output directory exists; create if not
    final_table.to_csv(OUTPUT_CSV_PATH, index=False) #save final merged data

    print("Pipeline completed successfully. Merged data saved to:", OUTPUT_CSV_PATH)

if __name__ == "__main__":
    run_pipeline()
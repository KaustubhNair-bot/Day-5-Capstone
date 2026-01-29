import pandas as pd
import numpy as np
import json
import glob
from .data_loader import load_cities
from .data_cleaner import clean_city_data

def transform_weather_data():
    #load and clean city data
    data = load_cities()
    cleaned_data = clean_city_data(data)

    #data to be appended in this list
    data_list = []

    #all json files in raw data folder
    weather_files = glob.glob('data/raw/*_weather.json')

    #read each json file and extract relevant info
    for file in weather_files:
        with open(file,'r') as f:
            weather_data = json.load(f)
            city = weather_data.get("name", " ").lower().strip()
            temp = weather_data.get("main", {}).get("temp", None)
            humidity = weather_data.get("main", {}).get("humidity", None)
            condition = weather_data.get("weather", [{}])[0].get("main", " ")

            data_list.append({
                "city": city,
                "temperature": temp,
                "humidity": humidity,
                "condition": condition
            })

    #create a dataframe from json list
    weather_df = pd.DataFrame(data_list)

    #merge data from api json with cleaned city data csv
    merged_df = pd.merge(cleaned_data, weather_df, on="city", how="inner")

    #add a derived column for temperature category
    merged_df['temperature_category'] = np.where(merged_df['temperature'] < 15, 'Cold', 
                                      np.where(merged_df['temperature'] <= 25, 'Moderate', 'Hot'))

    #add a derived column for population bucket
    bins=[0, 1_000_000, 5_000_000, 10_000_000, float('inf')]
    labels=['0M-1M', '1M-5M', '5M-10M', '10M+']

    merged_df['population_bucket']  = pd.cut(merged_df['population'], bins= bins, labels=labels, right=False)

    merged_df.columns = merged_df.columns.str.strip().str.lower()  # Ensure consistency

    merged_df.to_csv("data/processed/merged.csv", index=False)

    return merged_df

if __name__ == "__main__":  
    final_df = transform_weather_data()
    print(final_df.head())

    print(f"Total records after transformation: {len(final_df)}")
    
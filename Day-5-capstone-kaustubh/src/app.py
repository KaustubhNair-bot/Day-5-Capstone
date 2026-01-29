import os
import math
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import pandas as pd
from dotenv import load_dotenv

# Import our data processing modules
from .api_client import OpenWeatherClient
from .data_loader import CityDataLoader
from .data_cleaner import DataCleaner
from .transformer import DataTransformer

load_dotenv()

app = FastAPI(
    title="Data Processing & Analytics Service",
    description="REST API for city and weather data analytics",
    version="1.0.0"
)

# Global variable to cache the dataset
_cached_data: Optional[pd.DataFrame] = None


@app.on_event("startup")
async def startup_event():
    """Run data pipeline on startup if processed data doesn't exist."""
    csv_path = "data/processed/merged_data.csv"
    
    # Only run pipeline if processed data doesn't exist
    if not os.path.exists(csv_path):
        print("\n" + "=" * 60)
        print("RUNNING DATA PIPELINE (First startup)")
        print("=" * 60)
        
        try:
            # Cities to fetch weather data for
            CITIES = ['London', 'New York', 'Tokyo', 'Mumbai', 'Sydney']
            
            # Step 1: Fetch weather data
            print("\n[1/5] Fetching weather data from OpenWeatherMap API...")
            weather_client = OpenWeatherClient()
            weather_data_list = []
            
            for city in CITIES:
                try:
                    print(f"  → Fetching weather for {city}...")
                    weather_response = weather_client.fetch_weather_by_city(city)
                    weather_client.save_raw_response(city, weather_response)
                    
                    transformer = DataTransformer()
                    weather_features = transformer.extract_weather_features(weather_response)
                    weather_data_list.append(weather_features)
                    print(f"    ✓ {city}: {weather_features['temperature']}°C")
                except Exception as e:
                    print(f"    ✗ Failed: {e}")
            
            if not weather_data_list:
                print("\n✗ Pipeline failed: No weather data fetched")
                return
            
            # Step 2: Load city data
            print("\n[2/5] Loading city data...")
            loader = CityDataLoader("data/raw/worldcities.csv")
            cities_df = loader.load_data()
            cities_df = cities_df[cities_df['population'] >= 1_000_000]
            print(f"  ✓ Loaded {len(cities_df)} cities")
            
            # Step 3: Clean data
            print("\n[3/5] Cleaning data...")
            cleaner = DataCleaner()
            cities_df = cleaner.clean_cities_data(cities_df)
            
            # Step 4: Merge datasets
            print("\n[4/5] Merging datasets...")
            merged_df = transformer.merge_weather_with_cities(cities_df, weather_data_list)
            
            if len(merged_df) == 0:
                print("\n✗ Pipeline failed: No matching cities")
                return
            
            # Step 5: Add features and save
            print("\n[5/5] Adding features and saving...")
            merged_df = transformer.add_derived_features(merged_df)
            os.makedirs("data/processed", exist_ok=True)
            transformer.save_to_csv(merged_df, csv_path)
            
            print("\n" + "=" * 60)
            print(f"✓ PIPELINE COMPLETE - {len(merged_df)} cities processed")
            print("=" * 60 + "\n")
            
        except Exception as e:
            print(f"\n✗ Pipeline failed: {e}\n")
    else:
        print(f"\n✓ Using existing dataset: {csv_path}\n")


def load_dataset():
    """Load the processed dataset from CSV."""
    global _cached_data
    
    if _cached_data is None:
        csv_path = "data/processed/merged_data.csv"
        
        if not os.path.exists(csv_path):
            raise HTTPException(
                status_code=404,
                detail="Dataset not found. Please restart the API server to run the pipeline."
            )
        
        _cached_data = pd.read_csv(csv_path)
    
    return _cached_data


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Data Processing & Analytics Service API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /cities": "Get all cities with optional filters",
            "GET /cities/{city_name}": "Get specific city details",
            "GET /stats": "Get summary statistics"
        },
        "filters": {
            "temp_category": "Filter by temperature category (Cold, Moderate, Hot)",
            "population_bucket": "Filter by population bucket (Small, Medium, Large)",
            "country": "Filter by country name"
        }
    }


@app.get("/cities")
def get_cities(
    temp_category: Optional[str] = Query(None, description="Temperature category: Cold, Moderate, Hot"),
    population_bucket: Optional[str] = Query(None, description="Population bucket: Small, Medium, Large"),
    country: Optional[str] = Query(None, description="Country name")
):
    """
    Get all cities with optional filtering.
    
    Query Parameters:
    - temp_category: Filter by temperature category
    - population_bucket: Filter by population size
    - country: Filter by country name
    """
    df = load_dataset()
    filtered_df = df.copy()

    # Apply filters (with null-safe string operations)
    if temp_category and 'temperature_category' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['temperature_category'].fillna('').str.lower() == temp_category.lower()
        ]

    if population_bucket and 'population_bucket' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['population_bucket'].fillna('').str.lower() == population_bucket.lower()
        ]

    if country and 'country' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['country'].fillna('').str.lower() == country.lower()
        ]

    # Convert to dict and replace NaN with None for JSON serialization
    result = filtered_df.to_dict('records')
    
    # Clean NaN values from the records
    for record in result:
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = None

    return {
        "count": len(result),
        "cities": result
    }


@app.get("/cities/{city_name}")
def get_city(city_name: str):
    """
    Get details for a specific city.
    
    Parameters:
    - city_name: Name of the city (case-insensitive)
    """
    df = load_dataset()

    # Search for city (case-insensitive, null-safe)
    city_df = df[df['city'].fillna('').str.lower() == city_name.lower()]

    if len(city_df) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city_name}' not found in dataset"
        )

    # Convert to dict
    result = city_df.iloc[0].to_dict()
    
    # Clean NaN values
    for key, value in result.items():
        if isinstance(value, float) and math.isnan(value):
            result[key] = None
    
    return result


@app.get("/stats")
def get_stats():
    """Get summary statistics for the dataset."""
    df = load_dataset()

    stats = {
        "total_cities": len(df),
        "countries": int(df['country'].nunique()) if 'country' in df.columns else 0
    }

    # Temperature statistics
    if 'temperature' in df.columns:
        stats["temperature"] = {
            "average": round(float(df['temperature'].mean()), 2),
            "min": round(float(df['temperature'].min()), 2),
            "max": round(float(df['temperature'].max()), 2)
        }

    # Temperature category distribution
    if 'temperature_category' in df.columns:
        stats["temperature_distribution"] = df['temperature_category'].value_counts().to_dict()

    # Population distribution
    if 'population_bucket' in df.columns:
        stats["population_distribution"] = df['population_bucket'].value_counts().to_dict()

    # Weather conditions
    if 'weather_condition' in df.columns:
        stats["weather_conditions"] = df['weather_condition'].value_counts().to_dict()

    # Top countries by city count
    if 'country' in df.columns:
        stats["top_countries"] = df['country'].value_counts().head(5).to_dict()

    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

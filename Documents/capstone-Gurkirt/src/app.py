from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from .transformer import transform_weather_data

app=FastAPI()

# Helper function to fetch transformed data
def get_transformed_data():
    transformed_data = transform_weather_data()
    return transformed_data.to_dict(orient="records")

# 1. Endpoint: GET /cities - Get all cities
@app.get("/cities")
async def get_cities():
    data = get_transformed_data()
    return data

# 2. Endpoint: GET /cities/{city_name} - Get data for a specific city
@app.get("/cities/{city_name}")
async def get_city_data(city_name: str):
    data = get_transformed_data()
    city_data = [record for record in data if record["city"].lower() == city_name.lower()]
    if not city_data:
        return {"message": "City not found"}
    return city_data[0]

# 3. Endpoint: GET /cities?temp_category={category} - Get cities by temperature category
@app.get("/cities")
async def get_cities_by_temp_category(temp_category: str):
    data = get_transformed_data()

    if temp_category:
        temp_category = temp_category.lower()
        filtered_data = [city for city in data if city['temperature_category'].lower() == temp_category]
        
        if filtered_data:
            return filtered_data
        else:
            return {"error": f"No cities found with temperature category {temp_category}"}
    
    return data
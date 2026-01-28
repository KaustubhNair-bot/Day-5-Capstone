import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from enum import Enum

DATA_PATH = "data/processed/merged_data.csv"

app = FastAPI(title="City Weather Analytics API")


# ---------------- STARTUP CHECK ---------------- #

if not os.path.exists(DATA_PATH):
    raise HTTPException(
        status_code=500,
        detail="Processed data not found. Please run the data pipeline first."
    )

city_data = pd.read_csv(DATA_PATH)


# ---------------- ENUM FOR DROPDOWN ---------------- #

class TempCategory(str, Enum):
    Freezing = "Freezing"
    Cold = "Cold"
    Mild = "Mild"
    Warm = "Warm"
    Hot = "Hot"


# ---------------- ENDPOINTS ---------------- #

@app.get("/cities")
def get_cities(page: int = 1, limit: int = 10):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be positive integers."
        )

    start = (page - 1) * limit
    end = start + limit

    paged_table = city_data.iloc[start:end]

    return {
        "message": "Cities retrieved successfully.",
        "page": page,
        "limit": limit,
        "total_records": len(city_data),
        "data": paged_table.to_dict(orient="records")
    }


@app.get("/cities/by-temperature")
def get_cities_by_temperature(
    temp_category: TempCategory,
    page: int = 1,
    limit: int = 10
):
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be positive integers."
        )

    filtered = city_data[
        city_data["temp_category"] == temp_category.value
    ]

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No cities found for temperature category '{temp_category.value}'."
        )

    start = (page - 1) * limit
    end = start + limit

    paged_table = filtered.iloc[start:end]

    return {
        "message": f"Cities with temperature category '{temp_category.value}' retrieved successfully.",
        "temp_category": temp_category.value,
        "page": page,
        "limit": limit,
        "total_records": len(filtered),
        "data": paged_table.to_dict(orient="records")
    }


@app.get("/cities/{city_name}")
def get_city(city_name: str):
    city_name = city_name.lower()

    city_row = city_data[city_data["city"] == city_name]

    if city_row.empty:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city_name}' not found in the dataset."
        )

    return {
        "message": f"City '{city_name}' retrieved successfully.",
        "data": city_row.to_dict(orient="records")[0]
    }

@app.get("/insights/comparative-view")
def comparative_insights():
    if city_data.empty:
        raise HTTPException(
            status_code=500,
            detail="No data available to generate insights."
        )

    avg_temp = round(city_data["temp"].mean(), 2)
    avg_population = int(city_data["population"].mean())

    warmest = city_data.loc[city_data["temp"].idxmax()]
    coldest = city_data.loc[city_data["temp"].idxmin()]

    most_populated = city_data.loc[city_data["population"].idxmax()]
    least_populated = city_data.loc[city_data["population"].idxmin()]

    return {
        "message": "Comparative insights based on available city data",
        "dataset_average_temperature": avg_temp,
        "dataset_average_population": avg_population,
        "temperature_extremes": {
            "warmest_city": {
                "city": warmest["city"],
                "temperature": warmest["temp"]
            },
            "coldest_city": {
                "city": coldest["city"],
                "temperature": coldest["temp"]
            }
        },
        "population_extremes": {
            "most_populated_city": {
                "city": most_populated["city"],
                "population": int(most_populated["population"])
            },
            "least_populated_city": {
                "city": least_populated["city"],
                "population": int(least_populated["population"])
            }
        },
        "interpretation_note": (
            "All comparisons are relative to the cities included "
            "in the dataset and should not be interpreted as global rankings."
        )
    }

from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from contextlib import asynccontextmanager
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main_pipeline import run_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting up. Initializing fresh data...")
    try:
        run_pipeline()
        print("Data initialization successfull.")

    except Exception as e:
        print(f"Pipeline failed during startup: {e}")
        print("Continuing with existing data if available...")

    yield
    print("Server shutting down.")


# Initializing the FastAPI application
app = FastAPI(
    title="City Weather Analytics API",
    description="A professional-grade API serving fresh city weather and population data.",
    version="1.0.0",
    lifespan=lifespan,
)


def get_db_path():
    # Returns the path to the processed data file.
    return "data/processed/merged_data.csv"


def load_data():
    # Loads the CSV data or raises an error if it don't exist
    path = get_db_path()
    if not os.path.exists(path):
        raise HTTPException(
            status_code=500,
            detail="Database file not found. Ensure the pipeline runs at startup.",
        )

    return pd.read_csv(path)


@app.get("/")
def read_root():
    # Welcome endpoint
    return {
        "status": "online",
        "message": "Welcome to the Weather Analystics API",
        "docs": "/docs",
    }


# To get details of all cities while can also apply filter based on the temperature category
@app.get("/cities")
def get_all_cities(
    temp_category: str = Query(None, description="Filter by: Cold, Moderate, Hot"),
):
    df = load_data()

    if temp_category:
        category = temp_category.capitalize()
        df = df[df["temp_category"] == category]

        if df.empty:
            return {"message": f"No cities found for category: {category}", "data": []}

    return df.to_dict(orient="records")


# To get detail of particular city, if that city exits on the cleaned dataset
@app.get("/cities/{city_name}")
def get_city_by_name(city_name: str):
    # Fetches detailed data for a specific city.
    df = load_data()
    # Performing case-insensitive match
    result = df[df["city"] == city_name.lower()]

    if result.empty:
        raise HTTPException(
            status_code=404, detail=f"City {city_name} not found in our records."
        )

    return result.iloc[0].to_dict()

from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from pathlib import Path
from logger import get_logger

logger = get_logger("api")

app = FastAPI(title="City Weather Analytics API")

# Resolve project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "merged_data.csv"


def load_data() -> pd.DataFrame:
    """
    Load processed city-weather data.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Processed data not found. Please run pipeline.py first."
        )
    return pd.read_csv(DATA_PATH)

try:
    city_df = load_data()
except FileNotFoundError as e:
    city_df = pd.DataFrame()
    print(f"[ERROR] {e}")


@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.get("/cities")
def get_all_cities():
    """
    Get all cities.
    """
    logger.info("GET /cities called")
    if city_df.empty:
        raise HTTPException(status_code=500, detail="Data not loaded")

    return city_df.to_dict(orient="records")

@app.get("/cities/temp_category/{category}")
def get_cities_by_temp_category(category: str):
    """
    Get cities filtered by temperature category.
    """
    logger.info("GET /cities/temp_category called")
    if city_df.empty:
        raise HTTPException(status_code=500, detail="Data not loaded")

    df = city_df[city_df["temp_category"].str.lower() == category.lower()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No cities found for temp_category={category}"
        )

    return df.to_dict(orient="records")

@app.get("/cities/{city_name}")
def get_city(city_name: str):
    
    logger.info(f"GET /cities/{city_name} called")

    if city_df.empty:
        raise HTTPException(status_code=500, detail="Data not loaded")

    df = city_df[city_df["city"] == city_name.lower()]

    if df.empty:
        raise HTTPException(status_code=404, detail="City not found")

    return df.to_dict(orient="records")[0]



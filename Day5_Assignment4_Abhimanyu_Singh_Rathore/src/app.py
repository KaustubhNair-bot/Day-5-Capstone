

from fastapi import FastAPI, HTTPException
from src.config import (
    API_KEY,
    RAW_CSV_PATH,
    PROCESSED_CSV_PATH,
    TOP_N_CITIES,
    MIN_POPULATION
)

from src.data_loader import load_city_data, DataLoadError
from src.data_cleaner import clean_city_data, DataCleanError
from src.transformer import enrich_with_weather

app = FastAPI(title="City Weather Analytics API")

try:
    df = load_city_data(RAW_CSV_PATH)
    df = clean_city_data(df)

    df = df[df["population"] > MIN_POPULATION]
    df = df.sort_values(by="population", ascending=False).head(TOP_N_CITIES)

    final_df = enrich_with_weather(df, API_KEY)
    final_df.to_csv(PROCESSED_CSV_PATH, index=False)

except (DataLoadError, DataCleanError, RuntimeError) as e:
    # Stop app from running with bad data
    raise RuntimeError(f"Application startup failed: {e}")


@app.get("/cities")
def get_cities():
    return final_df.to_dict(orient="records")


@app.get("/cities/{city_name}")
def get_city(city_name: str):
    result = final_df[final_df["city"] == city_name.lower()]
    if result.empty:
        raise HTTPException(status_code=404, detail="City not found")
    return result.to_dict(orient="records")[0]


@app.get("/cities/filter")
def filter_by_temperature(temp_category: str):
    return final_df[
        final_df["temp_category"].str.lower() == temp_category.lower()
    ].to_dict(orient="records")

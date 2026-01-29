from logger import get_logger
from data_loader import load_city_data, prepare_city_payload
from data_cleaner import clean_city_data
from api_client import fetch_weather_for_cities
from transformer import merge_city_weather_data, save_final_dataset

logger = get_logger("pipeline")

def run_pipeline():
    logger.info("Starting data pipeline")

    logger.info("Loading city data")
    city_df = load_city_data(None)

    logger.info("Cleaning city data")
    city_df = clean_city_data(city_df)

    logger.info("Preparing city payload")
    cities_payload = prepare_city_payload(city_df, limit=5)

    logger.info("Fetching weather data")
    weather_data = fetch_weather_for_cities(cities_payload)

    logger.info("Merging datasets")
    final_df = merge_city_weather_data(city_df, weather_data)

    logger.info("Saving final dataset")
    save_final_dataset(final_df)

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()

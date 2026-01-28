import time

# Import your new modular classes
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.api_client import WeatherAPI
from src.transformer import DataProcessor


def run_pipeline():
    # Initializing the components
    loader = DataLoader()
    cleaner = DataCleaner()
    api = WeatherAPI()
    processor = DataProcessor()

    print("\n--- Initializing Fresh Data Pipeline ---")

    try:
        # Step 1: Loading the raw cities data
        raw_cities_df = loader.load_cities()
        if raw_cities_df is None:
            raise FileNotFoundError("Raw data source missing.")

        # Step 2: Clean the raw data
        cleaned_cities_df = cleaner.clean(raw_cities_df)
        # We take top 10 for the assignment scope
        top_cities = cleaned_cities_df.head(10)

        # Step 3: Fetch Fresh API Data
        print(f"Updating weather for {len(top_cities)} cities...")
        weather_results = []
        for _, row in top_cities.iterrows():
            city_name = row["city"]
            print(f" -> Refreshing: {city_name.capitalize()}...")

            weather_data = api.fetch_weather_data(city_name)
            if weather_data:
                weather_results.append(weather_data)

            # Free API Rate limit protection
            time.sleep(1)

        # Step 4: Transform & Overwrite Old File
        if not weather_results:
            raise Exception("API Connection failed. Could not refresh data.")

        processor.merge_and_transform(top_cities, weather_results)
        print("--- Data Refresh Successful ---\n")

    except Exception as e:
        print(f"PIPELINE ERROR: {e}")
        raise e


if __name__ == "__main__":
    run_pipeline()

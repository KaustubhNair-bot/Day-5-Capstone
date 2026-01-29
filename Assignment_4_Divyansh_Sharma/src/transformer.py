import pandas as pd
import os


class DataProcessor:
    def get_temp_category(self, temp):
        # Business Logic for Temperature Category.
        if temp < 15:
            return "Cold"
        elif 15 <= temp <= 25:
            return "Moderate"
        else:
            return "Hot"

    def get_pop_bucket(self, population):
        # Business Logic for Population Bucket.
        if population < 1000000:
            return "Small"
        elif 1000000 <= population <= 10000000:
            return "Medium"
        else:
            return "Large"

    def merge_and_transform(self, cities_df, weather_results):
        # Merges the two data sources and calculates derived columns.
        if not weather_results:
            return None

        weather_df = pd.DataFrame(weather_results)
        weather_df["city"] = weather_df["city"].str.lower()

        merged_df = pd.merge(cities_df, weather_df, on="city", validate="one_to_one")

        merged_df["temp_category"] = merged_df["temp"].apply(self.get_temp_category)
        merged_df["pop_bucket"] = merged_df["population"].apply(self.get_pop_bucket)

        # Ensuring directory exists and then saving the final processed data
        os.makedirs("data/processed", exist_ok=True)
        merged_df.to_csv("data/processed/merged_data.csv", index=False)

        return merged_df

import pandas as pd


class DataTransformer:
    """Handles data transformation and feature engineering."""

    @staticmethod
    def extract_weather_features(weather_data: dict) -> dict:
        """Extract relevant features from weather API response."""
        return {
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'weather_condition': weather_data['weather'][0]['main'],
            'weather_description': weather_data['weather'][0]['description']
        }

    @staticmethod
    def categorize_temperature(temp: float) -> str:
        """Categorize temperature as Cold, Moderate, or Hot."""
        if temp < 15:
            return 'Cold'
        elif temp <= 25:
            return 'Moderate'
        else:
            return 'Hot'

    @staticmethod
    def categorize_population(pop: float) -> str:
        """Categorize population as Small, Medium, or Large."""
        if pop < 1_000_000:
            return 'Small'
        elif pop <= 5_000_000:
            return 'Medium'
        else:
            return 'Large'

    def merge_weather_with_cities(
        self,
        cities_df: pd.DataFrame,
        weather_list: list
    ) -> pd.DataFrame:
        """Merge weather data with cities dataframe."""
        # Convert weather data to DataFrame
        weather_df = pd.DataFrame(weather_list)
        weather_df['city_normalized'] = weather_df['city'].str.lower()

        # Merge on normalized city names
        merged_df = pd.merge(
            cities_df,
            weather_df,
            on='city_normalized',
            how='inner',
            suffixes=('_city', '_weather')
        )

        # Use city name from cities dataset
        if 'city_city' in merged_df.columns:
            merged_df['city'] = merged_df['city_city']
            merged_df.drop(['city_city', 'city_weather'], axis=1, inplace=True, errors='ignore')

        return merged_df

    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add temperature and population categories."""
        df = df.copy()

        # Add temperature category
        if 'temperature' in df.columns:
            df['temperature_category'] = df['temperature'].apply(self.categorize_temperature)

        # Add population bucket
        if 'population' in df.columns:
            df['population_bucket'] = df['population'].apply(self.categorize_population)

        return df

    @staticmethod
    def save_to_csv(df: pd.DataFrame, filepath: str) -> None:
        """Save dataframe to CSV."""
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} rows to {filepath}")

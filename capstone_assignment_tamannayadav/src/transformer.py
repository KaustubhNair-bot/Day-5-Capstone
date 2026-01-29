"""
Transformer module for data transformations and feature engineering.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataTransformer:
    """Class for transforming and merging data."""
    
    def merge_weather_with_cities(self, cities_df, weather_data):
        """
        Merge weather data with cities DataFrame.
        
        Args:
            cities_df: DataFrame with cities data
            weather_data: List of weather data dictionaries
            
        Returns:
            pandas.DataFrame: Merged DataFrame
        """
        if cities_df is None or not weather_data:
            return None
        
        weather_df = pd.DataFrame(weather_data)
        weather_df['city'] = weather_df['city'].str.lower().str.strip()
        
        merged = cities_df.merge(
            weather_df[['city', 'temperature', 'humidity', 'weather_condition']],
            on='city',
            how='inner'
        )
        
        return merged
    
    def add_temperature_category(self, df, temp_column='temperature'):
        """
        Add temperature category column based on temperature values.
        
        Args:
            df: Input DataFrame
            temp_column: Name of temperature column
            
        Returns:
            pandas.DataFrame: DataFrame with temperature category
        """
        if df is None or temp_column not in df.columns:
            return df
        
        df = df.copy()
        
        def categorize_temp(temp):
            if pd.isna(temp):
                return 'Unknown'
            elif temp < 10:
                return 'Cold'
            elif temp < 25:
                return 'Moderate'
            else:
                return 'Hot'
        
        df['temp_category'] = df[temp_column].apply(categorize_temp)
        return df
    
    def add_population_bucket(self, df, pop_column='population'):
        """
        Add population bucket column based on population values.
        
        Args:
            df: Input DataFrame
            pop_column: Name of population column
            
        Returns:
            pandas.DataFrame: DataFrame with population bucket
        """
        if df is None or pop_column not in df.columns:
            return df
        
        df = df.copy()
        
        def categorize_population(pop):
            if pd.isna(pop):
                return 'Unknown'
            elif pop < 1000000:
                return 'Small'
            elif pop < 5000000:
                return 'Medium'
            elif pop < 10000000:
                return 'Large'
            else:
                return 'Mega'
        
        df['population_bucket'] = df[pop_column].apply(categorize_population)
        return df
    
    def transform_data(self, cities_df, weather_data):
        """
        Apply all transformations to the data.
        
        Args:
            cities_df: DataFrame with cities data
            weather_data: List of weather data dictionaries
            
        Returns:
            pandas.DataFrame: Fully transformed DataFrame
        """
        # Merge weather with cities
        df = self.merge_weather_with_cities(cities_df, weather_data)
        
        if df is None:
            return None
        
        # Add derived columns
        df = self.add_temperature_category(df)
        df = self.add_population_bucket(df)
        
        logger.info(f"Transformed data: {len(df)} rows with weather")
        return df


if __name__ == "__main__":
    # Test the transformer
    transformer = DataTransformer()
    
    # Sample cities data
    cities_df = pd.DataFrame({
        'city': ['tokyo', 'delhi', 'mumbai'],
        'country': ['Japan', 'India', 'India'],
        'lat': [35.68, 28.61, 19.07],
        'lng': [139.74, 77.23, 72.87],
        'population': [37785000, 32226000, 24973000]
    })
    
    # Sample weather data
    weather_data = [
        {'city': 'Tokyo', 'temperature': 15.5, 'humidity': 65, 'weather_condition': 'Clear sky'},
        {'city': 'Delhi', 'temperature': 28.0, 'humidity': 45, 'weather_condition': 'Partly cloudy'},
        {'city': 'Mumbai', 'temperature': 30.5, 'humidity': 75, 'weather_condition': 'Overcast'}
    ]
    
    result = transformer.transform_data(cities_df, weather_data)
    print("Transformed data:")
    print(result)

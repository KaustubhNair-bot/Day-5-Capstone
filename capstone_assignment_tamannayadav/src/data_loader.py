"""
Data Loader module for reading CSV and JSON files.
"""
import pandas as pd
import json
import os
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Class for loading data from CSV and JSON files."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "raw")
        self.processed_dir = os.path.join(data_dir, "processed")
    
    def load_cities_csv(self, filename="worldcities.csv"):
        """
        Load world cities data from CSV file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            pandas.DataFrame: Cities data
        """
        filepath = os.path.join(self.raw_dir, filename)
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} rows from {filepath}")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return None
        except pd.errors.EmptyDataError:
            logger.error(f"Empty file: {filepath}")
            return None
    
    def filter_cities(self, df, country=None, min_population=1000000):
        """
        Filter cities based on country and population.
        
        Args:
            df: DataFrame with cities data
            country: Country name to filter (optional)
            min_population: Minimum population threshold
            
        Returns:
            pandas.DataFrame: Filtered cities data
        """
        if df is None:
            return None
        
        filtered = df.copy()
        
        # Filter by population
        if min_population:
            filtered = filtered[filtered['population'] >= min_population]
        
        # Filter by country
        if country:
            filtered = filtered[filtered['country'] == country]
        
        return filtered
    
    def load_json(self, filepath):
        """
        Load data from JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            dict or list: Parsed JSON data
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file: {filepath}")
            return None
    
    def save_csv(self, df, filename):
        """
        Save DataFrame to CSV file in processed directory.
        
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        os.makedirs(self.processed_dir, exist_ok=True)
        filepath = os.path.join(self.processed_dir, filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved to {filepath}")


if __name__ == "__main__":
    # Test the data loader
    loader = DataLoader()
    
    df = loader.load_cities_csv()
    if df is not None:
        print(f"Total cities: {len(df)}")
        
        # Filter cities with population > 1 million
        filtered = loader.filter_cities(df, min_population=1000000)
        print(f"Cities with population > 1M: {len(filtered)}")
        
        # Filter Indian cities with population > 1 million
        indian_cities = loader.filter_cities(df, country="India", min_population=1000000)
        print(f"Indian cities with population > 1M: {len(indian_cities)}")

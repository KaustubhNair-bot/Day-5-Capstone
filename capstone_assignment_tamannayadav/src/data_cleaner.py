"""
Data Cleaner module for cleaning and normalizing data.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Class for cleaning and normalizing data."""
    
    def normalize_column_names(self, df):
        """
        Normalize column names to lowercase with underscores.
        
        Args:
            df: Input DataFrame
            
        Returns:
            pandas.DataFrame: DataFrame with normalized column names
        """
        df = df.copy()
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        return df
    
    def handle_missing_values(self, df, columns_to_check=None, strategy='drop'):
        """
        Handle missing values in the DataFrame.
        
        Args:
            df: Input DataFrame
            columns_to_check: List of columns to check for missing values
            strategy: 'drop' to remove rows, 'fill' to fill with defaults
            
        Returns:
            pandas.DataFrame: Cleaned DataFrame
        """
        df = df.copy()
        
        if columns_to_check is None:
            columns_to_check = df.columns.tolist()
        
        if strategy == 'drop':
            df = df.dropna(subset=columns_to_check)
        elif strategy == 'fill':
            for col in columns_to_check:
                if df[col].dtype in ['float64', 'int64']:
                    df[col] = df[col].fillna(0)
                else:
                    df[col] = df[col].fillna('Unknown')
        
        return df
    
    def remove_duplicates(self, df, subset=None):
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            df: Input DataFrame
            subset: Columns to consider for identifying duplicates
            
        Returns:
            pandas.DataFrame: DataFrame without duplicates
        """
        df = df.copy()
        df = df.drop_duplicates(subset=subset)
        return df
    
    def normalize_city_names(self, df, city_column='city'):
        """
        Normalize city names to lowercase.
        
        Args:
            df: Input DataFrame
            city_column: Name of the city column
            
        Returns:
            pandas.DataFrame: DataFrame with normalized city names
        """
        df = df.copy()
        if city_column in df.columns:
            df[city_column] = df[city_column].str.lower().str.strip()
        return df
    
    def clean_cities_data(self, df):
        """
        Apply all cleaning operations to cities data.
        
        Args:
            df: Input DataFrame with cities data
            
        Returns:
            pandas.DataFrame: Cleaned DataFrame
        """
        if df is None:
            return None
        
        # Normalize column names
        df = self.normalize_column_names(df)
        
        # Drop rows with missing lat/lng
        df = self.handle_missing_values(df, columns_to_check=['lat', 'lng'])
        
        # Normalize city names first (so duplicates like 'DELHI' and 'Delhi' are caught)
        df = self.normalize_city_names(df)
        
        # Remove duplicates based on city and country
        df = self.remove_duplicates(df, subset=['city', 'country'])
        
        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df


if __name__ == "__main__":
    # Test the data cleaner
    cleaner = DataCleaner()
    
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'City': ['Tokyo', 'Delhi', 'Delhi', 'Mumbai', None],
        'Country': ['Japan', 'India', 'India', 'India', 'Unknown'],
        'Lat': [35.68, 28.61, 28.61, 19.07, None],
        'Lng': [139.74, 77.23, 77.23, 72.87, None],
        'Population': [37785000, 32226000, 32226000, 24973000, 1000]
    })
    
    print("Original data:")
    print(sample_data)
    
    cleaned = cleaner.clean_cities_data(sample_data)
    print("\nCleaned data:")
    print(cleaned)

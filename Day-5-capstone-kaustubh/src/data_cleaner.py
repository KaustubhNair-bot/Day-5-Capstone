import pandas as pd


class DataCleaner:
    """Handles data cleaning operations."""

    @staticmethod
    def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Convert column names to lowercase."""
        df.columns = df.columns.str.lower()
        return df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame, required_columns: list) -> pd.DataFrame:
        """Drop rows with missing values in required columns."""
        return df.dropna(subset=required_columns)

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
        """Remove duplicate rows."""
        return df.drop_duplicates(subset=subset)

    @staticmethod
    def standardize_city_names(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize city names for consistent matching."""
        df['city'] = df['city'].str.strip()
        df['city_normalized'] = df['city'].str.lower()
        return df

    def clean_cities_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all cleaning steps to cities dataset."""
        # Normalize column names
        df = self.normalize_column_names(df)
        
        # Standardize city names
        df = self.standardize_city_names(df)
        
        # Remove rows with missing critical data
        required_columns = ['city', 'country', 'lat', 'lng']
        df = self.handle_missing_values(df, required_columns)
        
        # Remove duplicates
        df = self.remove_duplicates(df, subset=['city', 'country'])
        
        return df

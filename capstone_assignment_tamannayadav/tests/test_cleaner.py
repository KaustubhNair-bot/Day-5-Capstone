"""
Unit tests for data_cleaner module.
"""
import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):
    """Test cases for DataCleaner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cleaner = DataCleaner()
        
        # Sample test data
        self.sample_df = pd.DataFrame({
            'City': ['Tokyo', 'Delhi', 'Mumbai', 'London'],
            'Country': ['Japan', 'India', 'India', 'UK'],
            'Lat': [35.68, 28.61, 19.07, 51.50],
            'Lng': [139.74, 77.23, 72.87, -0.12],
            'Population': [37785000, 32226000, 24973000, 8982000]
        })
    
    def test_normalize_column_names(self):
        """Test that column names are normalized to lowercase."""
        result = self.cleaner.normalize_column_names(self.sample_df)
        
        expected_columns = ['city', 'country', 'lat', 'lng', 'population']
        self.assertEqual(list(result.columns), expected_columns)
    
    def test_handle_missing_values_drop(self):
        """Test that rows with missing values are dropped."""
        df_with_nulls = pd.DataFrame({
            'city': ['Tokyo', 'Delhi', None, 'London'],
            'lat': [35.68, None, 19.07, 51.50],
            'lng': [139.74, 77.23, 72.87, -0.12]
        })
        
        result = self.cleaner.handle_missing_values(
            df_with_nulls, 
            columns_to_check=['city', 'lat', 'lng'],
            strategy='drop'
        )
        
        self.assertEqual(len(result), 2)  # Only Tokyo and London should remain
    
    def test_handle_missing_values_fill(self):
        """Test that missing values are filled correctly."""
        df_with_nulls = pd.DataFrame({
            'city': ['Tokyo', None],
            'population': [37785000, None]
        })
        
        result = self.cleaner.handle_missing_values(
            df_with_nulls,
            columns_to_check=['city', 'population'],
            strategy='fill'
        )
        
        self.assertEqual(result.loc[1, 'city'], 'Unknown')
        self.assertEqual(result.loc[1, 'population'], 0)
    
    def test_remove_duplicates(self):
        """Test that duplicate rows are removed."""
        df_with_duplicates = pd.DataFrame({
            'city': ['Tokyo', 'Delhi', 'Delhi', 'Mumbai'],
            'country': ['Japan', 'India', 'India', 'India']
        })
        
        result = self.cleaner.remove_duplicates(df_with_duplicates, subset=['city', 'country'])
        
        self.assertEqual(len(result), 3)
    
    def test_normalize_city_names(self):
        """Test that city names are normalized to lowercase."""
        df = pd.DataFrame({
            'city': ['TOKYO', 'Delhi', '  Mumbai  ']
        })
        
        result = self.cleaner.normalize_city_names(df)
        
        self.assertEqual(result.loc[0, 'city'], 'tokyo')
        self.assertEqual(result.loc[1, 'city'], 'delhi')
        self.assertEqual(result.loc[2, 'city'], 'mumbai')
    
    def test_clean_cities_data_full_pipeline(self):
        """Test the full cleaning pipeline."""
        df = pd.DataFrame({
            'City': ['Tokyo', 'DELHI', 'Delhi', 'Mumbai'],
            'Country': ['Japan', 'India', 'India', 'India'],
            'Lat': [35.68, 28.61, 28.61, 19.07],
            'Lng': [139.74, 77.23, 77.23, 72.87],
            'Population': [37785000, 32226000, 32226000, 24973000]
        })
        
        result = self.cleaner.clean_cities_data(df)
        
        # Check column names are lowercase
        self.assertIn('city', result.columns)
        
        # Check duplicates removed
        self.assertEqual(len(result), 3)
        
        # Check city names are lowercase
        self.assertTrue(all(result['city'].str.islower()))


if __name__ == '__main__':
    unittest.main()

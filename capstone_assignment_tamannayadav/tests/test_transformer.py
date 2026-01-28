"""
Unit tests for transformer module.
"""
import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.transformer import DataTransformer


class TestDataTransformer(unittest.TestCase):
    """Test cases for DataTransformer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transformer = DataTransformer()
        
        # Sample cities data
        self.cities_df = pd.DataFrame({
            'city': ['tokyo', 'delhi', 'mumbai'],
            'country': ['Japan', 'India', 'India'],
            'lat': [35.68, 28.61, 19.07],
            'lng': [139.74, 77.23, 72.87],
            'population': [37785000, 32226000, 24973000]
        })
        
        # Sample weather data
        self.weather_data = [
            {'city': 'Tokyo', 'temperature': 8.0, 'humidity': 65, 'weather_condition': 'Clear'},
            {'city': 'Delhi', 'temperature': 18.0, 'humidity': 45, 'weather_condition': 'Cloudy'},
            {'city': 'Mumbai', 'temperature': 30.0, 'humidity': 75, 'weather_condition': 'Hot'}
        ]
    
    def test_merge_weather_with_cities(self):
        """Test merging weather data with cities DataFrame."""
        result = self.transformer.merge_weather_with_cities(self.cities_df, self.weather_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertIn('temperature', result.columns)
        self.assertIn('humidity', result.columns)
        self.assertIn('weather_condition', result.columns)
    
    def test_add_temperature_category_cold(self):
        """Test temperature category for cold temperatures."""
        df = pd.DataFrame({'temperature': [5.0, 8.0, 9.9]})
        
        result = self.transformer.add_temperature_category(df)
        
        self.assertTrue(all(result['temp_category'] == 'Cold'))
    
    def test_add_temperature_category_moderate(self):
        """Test temperature category for moderate temperatures."""
        df = pd.DataFrame({'temperature': [10.0, 15.0, 24.9]})
        
        result = self.transformer.add_temperature_category(df)
        
        self.assertTrue(all(result['temp_category'] == 'Moderate'))
    
    def test_add_temperature_category_hot(self):
        """Test temperature category for hot temperatures."""
        df = pd.DataFrame({'temperature': [25.0, 30.0, 40.0]})
        
        result = self.transformer.add_temperature_category(df)
        
        self.assertTrue(all(result['temp_category'] == 'Hot'))
    
    def test_add_population_bucket_small(self):
        """Test population bucket for small cities."""
        df = pd.DataFrame({'population': [500000, 999999]})
        
        result = self.transformer.add_population_bucket(df)
        
        self.assertTrue(all(result['population_bucket'] == 'Small'))
    
    def test_add_population_bucket_medium(self):
        """Test population bucket for medium cities."""
        df = pd.DataFrame({'population': [1000000, 3000000, 4999999]})
        
        result = self.transformer.add_population_bucket(df)
        
        self.assertTrue(all(result['population_bucket'] == 'Medium'))
    
    def test_add_population_bucket_large(self):
        """Test population bucket for large cities."""
        df = pd.DataFrame({'population': [5000000, 7000000, 9999999]})
        
        result = self.transformer.add_population_bucket(df)
        
        self.assertTrue(all(result['population_bucket'] == 'Large'))
    
    def test_add_population_bucket_mega(self):
        """Test population bucket for mega cities."""
        df = pd.DataFrame({'population': [10000000, 20000000, 37000000]})
        
        result = self.transformer.add_population_bucket(df)
        
        self.assertTrue(all(result['population_bucket'] == 'Mega'))
    
    def test_transform_data_full_pipeline(self):
        """Test the full transformation pipeline."""
        result = self.transformer.transform_data(self.cities_df, self.weather_data)
        
        self.assertIsNotNone(result)
        self.assertIn('temp_category', result.columns)
        self.assertIn('population_bucket', result.columns)
        
        # Check that categories are assigned correctly
        tokyo_row = result[result['city'] == 'tokyo'].iloc[0]
        self.assertEqual(tokyo_row['temp_category'], 'Cold')
        self.assertEqual(tokyo_row['population_bucket'], 'Mega')


if __name__ == '__main__':
    unittest.main()

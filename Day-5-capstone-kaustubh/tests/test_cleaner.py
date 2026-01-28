import pytest
import pandas as pd
from src.data_cleaner import DataCleaner


class TestDataCleaner:
    """Test cases for DataCleaner class."""

    @pytest.fixture
    def sample_df(self):
        """Create a sample dataframe for testing."""
        return pd.DataFrame({
            'City': ['  London  ', 'PARIS', 'tokyo', 'New York'],
            'Country': ['UK', 'France', 'Japan', 'USA'],
            'Lat': [51.5074, 48.8566, 35.6762, 40.7128],
            'Lng': [-0.1278, 2.3522, 139.6503, -74.0060],
            'Population': [9000000, 2161000, 13960000, 8336000]
        })

    def test_normalize_column_names(self, sample_df):
        """Test column name normalization to lowercase."""
        cleaner = DataCleaner()
        result = cleaner.normalize_column_names(sample_df)
        
        assert all(col.islower() for col in result.columns)
        assert 'city' in result.columns
        assert 'country' in result.columns

    def test_handle_missing_values(self):
        """Test missing value handling."""
        df = pd.DataFrame({
            'city': ['London', None, 'Tokyo'],
            'country': ['UK', 'France', 'Japan'],
            'lat': [51.5, 48.8, None],
            'lng': [-0.12, 2.35, 139.65]
        })
        
        cleaner = DataCleaner()
        result = cleaner.handle_missing_values(df, required_columns=['city', 'lat'])
        
        # Should remove rows with None in city or lat
        assert len(result) == 1
        assert result.iloc[0]['city'] == 'London'

    def test_remove_duplicates(self):
        """Test duplicate removal."""
        df = pd.DataFrame({
            'city': ['London', 'Paris', 'London', 'Tokyo'],
            'country': ['UK', 'France', 'UK', 'Japan']
        })
        
        cleaner = DataCleaner()
        result = cleaner.remove_duplicates(df, subset=['city', 'country'])
        
        assert len(result) == 3
        assert list(result['city']) == ['London', 'Paris', 'Tokyo']

    def test_standardize_city_names(self):
        """Test city name standardization."""
        df = pd.DataFrame({
            'city': ['  London  ', 'PARIS', 'tokyo  ', 'New York']
        })
        
        cleaner = DataCleaner()
        result = cleaner.standardize_city_names(df)
        
        # Check trimming
        assert result.iloc[0]['city'] == 'London'
        
        # Check normalized column created
        assert 'city_normalized' in result.columns
        assert result.iloc[0]['city_normalized'] == 'london'
        assert result.iloc[1]['city_normalized'] == 'paris'

    def test_clean_cities_data_integration(self, sample_df):
        """Test complete cleaning pipeline."""
        cleaner = DataCleaner()
        result = cleaner.clean_cities_data(sample_df)
        
        # Check all columns are lowercase
        assert all(col.islower() for col in result.columns)
        
        # Check city_normalized exists
        assert 'city_normalized' in result.columns
        
        # Check no missing values in critical columns
        assert result['city'].notna().all()
        assert result['country'].notna().all()
        assert result['lat'].notna().all()
        assert result['lng'].notna().all()
        
        # Check city names are trimmed
        assert not any(result['city'].str.startswith(' '))
        assert not any(result['city'].str.endswith(' '))

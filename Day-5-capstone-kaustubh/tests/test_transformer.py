import pytest
import pandas as pd
from src.transformer import DataTransformer


class TestDataTransformer:
    """Test cases for DataTransformer class."""

    @pytest.fixture
    def sample_weather_data(self):
        """Sample weather API response."""
        return {
            'name': 'London',
            'main': {
                'temp': 18.5,
                'humidity': 65
            },
            'weather': [
                {
                    'main': 'Clouds',
                    'description': 'scattered clouds'
                }
            ]
        }

    @pytest.fixture
    def sample_cities_df(self):
        """Sample cities dataframe."""
        return pd.DataFrame({
            'city': ['London', 'Paris', 'Tokyo'],
            'city_normalized': ['london', 'paris', 'tokyo'],
            'country': ['UK', 'France', 'Japan'],
            'lat': [51.5074, 48.8566, 35.6762],
            'lng': [-0.1278, 2.3522, 139.6503],
            'population': [9000000, 2161000, 13960000]
        })

    def test_extract_weather_features(self, sample_weather_data):
        """Test weather feature extraction."""
        transformer = DataTransformer()
        features = transformer.extract_weather_features(sample_weather_data)
        
        assert features['city'] == 'London'
        assert features['temperature'] == 18.5
        assert features['humidity'] == 65
        assert features['weather_condition'] == 'Clouds'
        assert features['weather_description'] == 'scattered clouds'

    def test_categorize_temperature_cold(self):
        """Test cold temperature categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_temperature(10) == 'Cold'
        assert transformer.categorize_temperature(14.9) == 'Cold'

    def test_categorize_temperature_moderate(self):
        """Test moderate temperature categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_temperature(15) == 'Moderate'
        assert transformer.categorize_temperature(20) == 'Moderate'
        assert transformer.categorize_temperature(25) == 'Moderate'

    def test_categorize_temperature_hot(self):
        """Test hot temperature categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_temperature(25.1) == 'Hot'
        assert transformer.categorize_temperature(35) == 'Hot'

    def test_categorize_population_small(self):
        """Test small population categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_population(500000) == 'Small'
        assert transformer.categorize_population(999999) == 'Small'

    def test_categorize_population_medium(self):
        """Test medium population categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_population(1000000) == 'Medium'
        assert transformer.categorize_population(3000000) == 'Medium'
        assert transformer.categorize_population(5000000) == 'Medium'

    def test_categorize_population_large(self):
        """Test large population categorization."""
        transformer = DataTransformer()
        
        assert transformer.categorize_population(5000001) == 'Large'
        assert transformer.categorize_population(10000000) == 'Large'

    def test_merge_weather_with_cities(self, sample_cities_df):
        """Test merging weather data with cities dataframe."""
        transformer = DataTransformer()
        
        weather_list = [
            {
                'city': 'London',
                'temperature': 18.5,
                'humidity': 65,
                'weather_condition': 'Clouds',
                'weather_description': 'scattered clouds'
            },
            {
                'city': 'Tokyo',
                'temperature': 22.3,
                'humidity': 70,
                'weather_condition': 'Clear',
                'weather_description': 'clear sky'
            }
        ]
        
        result = transformer.merge_weather_with_cities(sample_cities_df, weather_list)
        
        # Should match 2 cities (London and Tokyo)
        assert len(result) == 2
        assert 'temperature' in result.columns
        assert 'humidity' in result.columns
        assert 'weather_condition' in result.columns

    def test_add_derived_features(self):
        """Test adding temperature and population categories."""
        transformer = DataTransformer()
        
        df = pd.DataFrame({
            'city': ['London', 'Tokyo', 'Mumbai'],
            'temperature': [12, 20, 30],
            'population': [900000, 3500000, 12500000]
        })
        
        result = transformer.add_derived_features(df)
        
        # Check temperature categories
        assert 'temperature_category' in result.columns
        assert result.iloc[0]['temperature_category'] == 'Cold'
        assert result.iloc[1]['temperature_category'] == 'Moderate'
        assert result.iloc[2]['temperature_category'] == 'Hot'
        
        # Check population buckets
        assert 'population_bucket' in result.columns
        assert result.iloc[0]['population_bucket'] == 'Small'
        assert result.iloc[1]['population_bucket'] == 'Medium'
        assert result.iloc[2]['population_bucket'] == 'Large'

    def test_edge_case_boundary_temperature(self):
        """Test temperature categorization at boundary values."""
        transformer = DataTransformer()
        
        assert transformer.categorize_temperature(15.0) == 'Moderate'
        assert transformer.categorize_temperature(25.0) == 'Moderate'

    def test_edge_case_boundary_population(self):
        """Test population categorization at boundary values."""
        transformer = DataTransformer()
        
        assert transformer.categorize_population(1000000) == 'Medium'
        assert transformer.categorize_population(5000000) == 'Medium'

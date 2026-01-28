import pytest
from unittest.mock import Mock, patch
from src.api_client import OpenWeatherClient


class TestAPIClient:
    """Test cases for OpenWeatherClient."""

    @pytest.fixture
    def mock_response(self):
        """Mock successful API response."""
        return {
            'name': 'London',
            'main': {
                'temp': 18.5,
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [
                {
                    'main': 'Clouds',
                    'description': 'scattered clouds'
                }
            ],
            'wind': {
                'speed': 5.5
            }
        }

    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_api_key'})
    def test_client_initialization_with_env_key(self):
        """Test client initialization with environment variable."""
        client = OpenWeatherClient()
        assert client.api_key == 'test_api_key'

    def test_client_initialization_without_key(self):
        """Test client initialization fails without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OPENWEATHER_API_KEY not found"):
                OpenWeatherClient()

    @patch('src.api_client.requests.get')
    @patch.dict('os.environ', {'OPEN WEATHER_API_KEY': 'test_api_key'})
    def test_fetch_weather_success(self, mock_get, mock_response):
        """Test successful weather data fetching."""
        # Mock successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        client = OpenWeatherClient()
        result = client.fetch_weather_by_city('London')
        
        assert result['name'] == 'London'
        assert result['main']['temp'] == 18.5
        
        # Verify API call was made correctly
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs['params']['q'] == 'London'
        assert call_kwargs['params']['units'] == 'metric'

    @patch('src.api_client.requests.get')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_api_key'})
    def test_fetch_weather_api_error(self, mock_get):
        """Test handling of API errors."""
        # Mock failed response
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'City not found'
        
        client = OpenWeatherClient()
        
        with pytest.raises(RuntimeError, match="API request failed"):
            client.fetch_weather_by_city('InvalidCity')

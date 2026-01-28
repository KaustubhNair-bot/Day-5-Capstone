"""
REST API module using Flask for exposing processed data.
"""
from flask import Flask, jsonify, request
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from src.api_client import WeatherAPIClient
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.transformer import DataTransformer

app = Flask(__name__)

# Global variable to store processed data
processed_data = None


def initialize_data():
    """Load and process data on startup."""
    global processed_data
    
    logger.info("Starting data initialization...")
    
    # Initialize components
    loader = DataLoader()
    cleaner = DataCleaner()
    transformer = DataTransformer()
    api_client = WeatherAPIClient()
    
    # Load and clean cities data
    cities_df = loader.load_cities_csv()
    if cities_df is None:
        logger.error("Failed to load cities data")
        return
    
    cities_df = cleaner.clean_cities_data(cities_df)
    
    # Filter cities with population > 1 million
    cities_df = loader.filter_cities(cities_df, min_population=1000000)
    
    # Select 5 cities for weather data
    sample_cities = cities_df.head(5).to_dict('records')
    cities_for_weather = [
        {"city": row['city'], "lat": row['lat'], "lng": row['lng']}
        for row in sample_cities
    ]
    
    # Fetch weather data
    weather_data = api_client.fetch_weather_for_cities(cities_for_weather)
    
    # Save raw weather response
    api_client.save_raw_response(weather_data, "data/raw/weather_response.json")
    
    # Transform and merge data
    processed_data = transformer.transform_data(cities_df, weather_data)
    
    if processed_data is not None:
        # Save processed data
        loader.save_csv(processed_data, "merged_data.csv")
        logger.info(f"Processed {len(processed_data)} cities with weather data")


@app.route('/')
def home():
    """Home endpoint with API info."""
    return jsonify({
        "message": "Data Processing & Analytics Service",
        "endpoints": {
            "GET /cities": "Get all cities with weather data",
            "GET /cities/<city_name>": "Get specific city data",
            "GET /cities?temp_category=Hot": "Filter cities by temperature category",
            "GET /cities?page=1&per_page=10": "Paginated results"
        }
    })


@app.route('/cities', methods=['GET'])
def get_cities():
    """Get all cities or filter by temperature category with pagination."""
    global processed_data
    
    if processed_data is None or processed_data.empty:
        return jsonify({"error": "No data available"}), 404
    
    # Check for temp_category filter
    temp_category = request.args.get('temp_category')
    
    result_df = processed_data.copy()
    
    if temp_category:
        result_df = result_df[result_df['temp_category'].str.lower() == temp_category.lower()]
    
    if result_df.empty:
        return jsonify({"message": "No cities found matching criteria", "data": []}), 200
    
    # Pagination
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    total = len(result_df)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_df = result_df.iloc[start:end]
    result = paginated_df.to_dict('records')
    
    logger.info(f"GET /cities - page={page}, per_page={per_page}, total={total}")
    
    return jsonify({
        "count": len(result),
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
        "data": result
    })


@app.route('/cities/<city_name>', methods=['GET'])
def get_city(city_name):
    """Get data for a specific city."""
    global processed_data
    
    if processed_data is None or processed_data.empty:
        return jsonify({"error": "No data available"}), 404
    
    # Search for city (case-insensitive)
    city_data = processed_data[processed_data['city'].str.lower() == city_name.lower()]
    
    if city_data.empty:
        return jsonify({"error": f"City '{city_name}' not found"}), 404
    
    result = city_data.to_dict('records')[0]
    
    return jsonify(result)


if __name__ == "__main__":
    logger.info("Initializing data...")
    initialize_data()
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5000, host='0.0.0.0')

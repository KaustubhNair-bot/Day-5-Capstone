# DAY 5 - CAPSTONE

## Project Overview

The City Weather API is a FastAPI-based application that allows users to fetch weather data for cities around the world. The application integrates with the OpenWeatherMap API to collect real-time weather data and merges this data with city information (like population, latitude, and longitude). This data is then exposed through multiple API endpoints that allow users to query cities by name, temperature category (Cold, Moderate, Hot), or by other criteria.

The application processes and cleans city data from a CSV file, fetches weather information, and serves this data via RESTful API endpoints.

## Setup Instructions

### Steps to Set Up:

1. **Clone the Repository**:
   git clone https://github.com/your-username/city-weather-api.git
   cd city-weather-api

2. **Create a Virtual Environment**:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies**:
Install the required Python packages listed in requirements.txt:

pip install -r requirements.txt

4. **Set Up Environment Variables**:
Create a .env file in the project root directory and add the OpenWeatherMap API key:
OPENWEATHER_API_KEY=your_api_key_here

5. **Download City Data**:
Ensure you have the worldcities.csv file in the data/raw directory. This file contains city information that will be cleaned and merged with the weather data.

6. **Run the Application**:
To start the FastAPI application, run:
uvicorn app:app --reload
This will start the server on http://127.0.0.1:8000.

## API Usage Examples

Once the application is running, you can interact with the API through the following endpoints:

1. **Get All Cities**

Endpoint: /cities
Method: GET
This endpoint retrieves all cities with weather data.

Example Request:
curl http://127.0.0.1:8000/cities

Response:
[
  {
    "city": "new york",
    "country": "usa",
    "lat": 40.7128,
    "lng": -74.0060,
    "population": 8000000,
    "temperature": 20,
    "humidity": 80,
    "condition": "Clear",
    "temperature_category": "Moderate",
    "population_bucket": "5M-10M"
  },
  ...
]

2. **Get City Data by Name**

Endpoint: /cities/{city_name}
Method: GET
Fetches weather data for a specific city by name.

Example Request:
curl http://127.0.0.1:8000/cities/new%20york

Response:
{
  "city": "new york",
  "country": "usa",
  "lat": 40.7128,
  "lng": -74.0060,
  "population": 8000000,
  "temperature": 20,
  "humidity": 80,
  "condition": "Clear",
  "temperature_category": "Moderate",
  "population_bucket": "5M-10M"
}

3. **Get Cities by Temperature Category**

Endpoint: /cities?temp_category={category}
Method: GET
Fetches all cities that match the specified temperature category.

Example Request:
curl http://127.0.0.1:8000/cities?temp_category=moderate

Response:
[
  {
    "city": "new york",
    "country": "usa",
    "lat": 40.7128,
    "lng": -74.0060,
    "population": 8000000,
    "temperature": 20,
    "humidity": 80,
    "condition": "Clear",
    "temperature_category": "Moderate",
    "population_bucket": "5M-10M"
  },
  ...
]

## What Was Implemented

1. Weather Data Fetching: Integrated OpenWeatherMap API to fetch weather data for a list of cities.

2. Data Transformation Pipeline: Cleaned and merged weather data with city information (latitude, longitude, population, etc.).

3. FastAPI Endpoints: Exposed RESTful API endpoints to retrieve city weather data and filter by temperature category.

4. Data Cleaning: Filtered out cities with missing data and removed duplicates.

5. Tests: Unit tests for data cleaning, transformation, and API behavior using pytest.

## Known Limitations

1. API Rate Limits: OpenWeatherMap API has rate limits that might restrict the number of requests. Ensure that you are using a paid API plan if you need a higher request limit.

2. Weather Data Availability: If weather data for a city is not available (e.g., due to an incorrect city name or API issue), the API will return a message indicating that the city was not found.

3. Data Refreshing: The weather data is not dynamically refreshed in real-time. The app fetches data once and stores it, meaning that the data might be outdated unless updated manually.

4. Large Datasets: If the dataset grows too large (i.e., many cities with weather data), the system could slow down or require additional resources for processing and storage.


## Next Steps

1. Caching: Implement caching mechanisms (e.g., using Redis) to store weather data for frequently queried cities to reduce API calls and improve performance.

2. Pagination: Implement pagination for the /cities endpoint to handle large datasets and improve API response times.

3. Error Handling: Improve error handling for network issues, invalid API responses, and missing weather data.

4. Deploy: Deploy the application to a cloud platform like AWS, Azure, or Heroku for public access.

5. Advanced Weather Data: Integrate additional weather data points such as wind speed, air pressure, or weather forecasts.


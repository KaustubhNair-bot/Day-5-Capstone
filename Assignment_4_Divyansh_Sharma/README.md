City Weather Analytics API

A modular, high-performance Python data pipeline and FastAPI application that fetches real-time weather data for global cities, processes population metrics, and serves the results through a RESTful API. 


Project Overview
This project automates the transition from raw urban data to actionable insights. It includes:

1. Modular Pipeline
Separate components for Data Ingestion, Cleaning, and Transformation.

2. Live Data Refresh
Automatically refreshes weather data using the OpenWeatherMap API on server startup via FastAPI Lifespan events.

3. Categorization Engine
Business logic to bucket cities based on:
 . Temperature: Hot, Moderate, Cold
 . Population: Large, Medium, Small

4. Automated Testing
Comprehensive unit tests to ensure data accuracy and integrity.


Setup & Installation
1. Clone the Project
cd Assignment_4

2. Environment Configuration
Create a .env file in the root directory and add your API key:
 . WEATHER_API_KEY=your_openweathermap_api_key_here

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
The server automatically triggers the data pipeline on startup to ensure fresh data.
 . fastapi dev src/app.py


API Usage
Once the server is running (default: http://127.0.0.1:8000), the following endpoints are available:

1. GET /cities
Retrieve the full list of processed cities.

2. GET /cities/{name}
Get detailed weather and population metrics for a specific city.

3. GET /cities?temp_category=Hot
Filter cities by temperature category (Hot, Moderate, Cold).

Access Swagger UI to explore and test endpoints:
 . http://127.0.0.1:8000/docs


Testing
To validate data processing logic and cleaning rules, run:
 . python -m pytest
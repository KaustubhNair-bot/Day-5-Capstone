# Data Processing & Analytics Service

A Python-based data processing service that fetches real-time weather data from Open-Meteo API, combines it with world cities data, and exposes insights via REST APIs.

## Project Overview

This project demonstrates:
- API integration with Open-Meteo weather API
- CSV data loading and processing with pandas
- Data cleaning and transformation
- REST API development with Flask
- Unit testing with pytest

## Project Structure

```
day5-capstone/
├── data/
│   ├── raw/
│   │   └── worldcities.csv
│   └── processed/
│       └── merged_data.csv
├── src/
│   ├── __init__.py
│   ├── api_client.py      # Weather API calls
│   ├── data_loader.py     # CSV/JSON readers
│   ├── data_cleaner.py    # Cleaning logic
│   ├── transformer.py     # Data transformations
│   └── app.py             # REST API
├── tests/
│   ├── test_cleaner.py
│   └── test_transformer.py
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd day5-capstone
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/app.py
   ```

## Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t data-service .
docker run -p 5000:5000 data-service
```

## API Usage

### Get all cities
```bash
GET http://localhost:5000/cities
```

### Get specific city
```bash
GET http://localhost:5000/cities/tokyo
```

### Filter by temperature category
```bash
GET http://localhost:5000/cities?temp_category=Hot
```

### Pagination
```bash
GET http://localhost:5000/cities?page=1&per_page=5
```

### Example Response
```json
{
  "count": 5,
  "total": 5,
  "page": 1,
  "per_page": 10,
  "total_pages": 1,
  "data": [
    {
      "city": "tokyo",
      "country": "Japan",
      "lat": 35.687,
      "lng": 139.7495,
      "population": 37785000,
      "temperature": 15.5,
      "humidity": 65,
      "weather_condition": "Clear sky",
      "temp_category": "Moderate",
      "population_bucket": "Mega"
    }
  ]
}
```

## Running Tests

```bash
pytest tests/ -v
```

## Data Sources

- **Weather Data**: [Open-Meteo API](https://open-meteo.com/) (No API key required)
- **Cities Data**: [World Cities Dataset](https://simplemaps.com/data/world-cities)

## Features Implemented

- Fetch real-time weather data for cities
- Load and filter world cities CSV data
- Clean data (normalize columns, handle nulls, remove duplicates)
- Transform data (merge datasets, add derived columns)
- REST API with filtering capabilities
- Unit tests for cleaner and transformer modules
- **Logging** across all modules (logs to `app.log`)
- **Pagination** support on `/cities` endpoint
- **Docker** support with Dockerfile and docker-compose.yml

## Known Limitations

- Weather data is fetched for top 5 cities by population only
- No authentication on API endpoints
- Data is loaded in memory on startup

## Next Steps

- Implement caching for weather data
- Add authentication to API endpoints
- Add more comprehensive error handling

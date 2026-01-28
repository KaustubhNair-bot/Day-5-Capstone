# Data Processing & Analytics Service

## 📋 Project Overview

A comprehensive data processing pipeline that integrates real-time weather data from the OpenWeatherMap API with a global cities dataset. The system performs data cleaning, transformation, and feature engineering, then exposes insights through a RESTful API built with FastAPI.

### Key Features

- **API Integration**: Fetches real-time weather data from OpenWeatherMap for multiple cities
- **Data Processing**: Loads, cleans, and transforms CSV data using pandas
- **Feature Engineering**: Creates derived features (temperature categories, population buckets)
- **REST API**: FastAPI endpoints for querying and filtering city/weather data
- **Unit Testing**: Comprehensive test coverage with pytest
- **Modular Design**: Object-oriented Python code with clear separation of concerns

---

## 🏗️ Project Structure

```
day5-capstone/
│
├── data/
│   ├── raw/
│   │   └── worldcities.csv          # Input CSV dataset
│   └── processed/
│       └── merged_data.csv           # Output merged dataset
│
├── src/
│   ├── __init__.py
│   ├── api_client.py                 # OpenWeatherMap API client
│   ├── data_loader.py                # CSV data loader
│   ├── data_cleaner.py               # Data cleaning utilities
│   ├── transformer.py                # Data transformation & feature engineering
│   └── app.py                        # FastAPI REST API (includes pipeline logic)
│
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py            # API client tests
│   ├── test_cleaner.py               # Data cleaner tests
│   └── test_transformer.py           # Transformer tests
│
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── .gitignore
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8+
- OpenWeatherMap API key (free tier)

### 2. Get OpenWeatherMap API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API keys section
4. Generate a new API key

### 3. Environment Setup

```bash
# Navigate to project directory
cd Day-5-capstone

# Create virtual environment
python -m venv cap_env

# Activate virtual environment
# On macOS/Linux:
source cap_env/bin/activate
# On Windows:
cap_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your API key:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

---

## 📊 Usage

### Start the API Server

The data pipeline runs **automatically** on first startup if processed data doesn't exist.

```bash
# Method 1: Direct execution
python src/app.py

# Method 2: Using uvicorn (recommended for development)
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

**What happens on first startup:**
1. Checks if `data/processed/merged_data.csv` exists
2. If not, automatically runs the data pipeline:
   - Fetches weather data for 5 cities (London, New York, Tokyo, Mumbai, Sydney)
   - Loads world cities CSV dataset
   - Cleans and standardizes data
   - Merges weather and city data
   - Adds derived features (temperature categories, population buckets)
   - Saves processed data to `data/processed/merged_data.csv`
3. Starts the API server

**Subsequent startups:**
- Uses the existing processed dataset
- Starts immediately without re-running the pipeline

The API will be available at `http://localhost:8000`

### API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### 1. Root Endpoint

```bash
GET /
```

Returns API information and available endpoints.

**Example:**
```bash
curl http://localhost:8000/
```

### 2. Get All Cities

```bash
GET /cities
```

Returns all cities with optional filtering.

**Query Parameters:**
- `temp_category` - Filter by temperature (Cold, Moderate, Hot)
- `population_bucket` - Filter by population (Small, Medium, Large)
- `country` - Filter by country name

**Examples:**
```bash
# Get all cities
curl http://localhost:8000/cities

# Get cities with hot temperature
curl http://localhost:8000/cities?temp_category=Hot

# Get large cities
curl http://localhost:8000/cities?population_bucket=Large

# Get cities in UK
curl http://localhost:8000/cities?country=UK
```

**Response:**
```json
{
  "count": 2,
  "cities": [
    {
      "city": "London",
      "country": "UK",
      "population": 9000000,
      "temperature": 18.5,
      "humidity": 65,
      "weather_condition": "Clouds",
      "temperature_category": "Moderate",
      "population_bucket": "Large"
    }
  ]
}
```

### 3. Get Specific City

```bash
GET /cities/{city_name}
```

Returns details for a specific city (case-insensitive).

**Example:**
```bash
curl http://localhost:8000/cities/London
```

**Response:**
```json
{
  "city": "London",
  "country": "UK",
  "lat": 51.5074,
  "lng": -0.1278,
  "population": 9000000,
  "temperature": 18.5,
  "humidity": 65,
  "weather_condition": "Clouds",
  "weather_description": "scattered clouds",
  "temperature_category": "Moderate",
  "population_bucket": "Large"
}
```

### 4. Get Statistics

```bash
GET /stats
```

Returns summary statistics for the entire dataset.

**Example:**
```bash
curl http://localhost:8000/stats
```

**Response:**
```json
{
  "total_cities": 5,
  "countries": 5,
  "temperature": {
    "average": 20.5,
    "min": 12.3,
    "max": 28.7
  },
  "temperature_distribution": {
    "Cold": 1,
    "Moderate": 2,
    "Hot": 2
  },
  "population_distribution": {
    "Large": 3,
    "Medium": 2
  }
}
```

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_cleaner.py -v
pytest tests/test_transformer.py -v
pytest tests/test_api_client.py -v
```

**Expected Output:**
```
tests/test_cleaner.py::TestDataCleaner::test_normalize_column_names PASSED
tests/test_cleaner.py::TestDataCleaner::test_handle_missing_values PASSED
tests/test_transformer.py::TestDataTransformer::test_categorize_temperature_cold PASSED
...
==================== X passed in X.XXs ====================
```

---

## 📐 Data Categories

### Temperature Categories

| Temperature (°C) | Category  |
|------------------|-----------|
| < 15             | Cold      |
| 15 - 25          | Moderate  |
| > 25             | Hot       |

### Population Buckets

| Population       | Bucket    |
|------------------|-----------|
| < 1,000,000      | Small     |
| 1M - 5M          | Medium    |
| > 5,000,000      | Large     |

---

## 🔧 Technology Stack

- **Python 3.8+**
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP library for API calls
- **Pytest** - Testing framework
- **python-dotenv** - Environment variable management

---

## 📝 Known Limitations

1. **City Matching**: Weather data is matched with city database using case-insensitive city names. Cities with different spellings or special characters may not match.

2. **API Rate Limits**: OpenWeatherMap free tier has rate limits (60 calls/minute). The pipeline includes small delays between requests.

3. **Static Cities**: Currently fetches weather for 5 predefined cities. Future versions could accept dynamic city lists.

4. **No Historical Data**: Only current weather data is fetched, not historical trends.

5. **Limited Error Recovery**: Pipeline stops on critical errors rather than attempting partial processing.

---

## 🚀 Future Enhancements

- [ ] **Docker Support**: Containerize the application for easy deployment
- [ ] **Logging**: Add structured logging with different log levels
- [ ] **Pagination**: Implement pagination for `/cities` endpoint
- [ ] **Caching**: Add Redis caching for API responses
- [ ] **Database**: Store processed data in PostgreSQL/MongoDB
- [ ] **Scheduled Updates**: Add cron jobs for periodic weather updates
- [ ] **More APIs**: Integrate additional data sources (pollution, traffic, etc.)
- [ ] **Authentication**: Add API key authentication for endpoints
- [ ] **Data Visualization**: Create dashboard with charts and graphs

---

## 👥 Contributing

### Git Workflow

1. Create feature branch: `git checkout -b feature/day5-assignment`
2. Make changes and commit: `git commit -m "Add feature X"`
3. Push branch: `git push origin feature/day5-assignment`
4. Create Pull Request on GitHub

### Commit Message Guidelines

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."
- Limit first line to 72 characters
- Reference issues and pull requests

---

## 📄 License

This project is created for educational purposes as part of Day 5 Capstone Assignment.

---

## 🆘 Troubleshooting

### API Key Not Found

```
ValueError: OPENWEATHER_API_KEY not found in environment variables
```

**Solution**: Ensure `.env` file exists with your API key

### Dataset Not Found

```
Dataset not found. Please restart the API server to run the pipeline.
```

**Solution**: 
- The pipeline runs automatically on first startup
- Make sure you have a valid `OPENWEATHER_API_KEY` in `.env`
- Restart the API server: `python src/app.py`
- Check console output for pipeline execution status

### Import Errors

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source cap_env/bin/activate
pip install -r requirements.txt
```

---

## 📧 Contact

For questions or issues, please raise an issue in the GitHub repository.

---

**Built with ❤️ using Python, FastAPI, and Pandas**

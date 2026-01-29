# City Weather Analytics API

A modular city weather analytics service built with Python and FastAPI that combines static city data with real-time weather information, processes data through a robust pipeline, and exposes insights via REST APIs.

## Features

- **Real-time Weather Integration**: Fetches live weather data from OpenWeather API
- **Intelligent Data Processing**: Cleans, transforms, and enriches city data
- **RESTful API**: Well-designed endpoints with pagination and filtering
- **Temperature Categorization**: Automatic classification into five temperature ranges
- **Population Bucketing**: Cities grouped by population size
- **Comparative Analytics**: Dataset-wide insights and statistics
- **Comprehensive Testing**: Unit tests for core functionality

## Tech Stack

- **Python** - Core programming language
- **FastAPI** - Modern web framework for building APIs
- **Pandas** - Data manipulation and analysis
- **Uvicorn** - ASGI server
- **Requests** - HTTP library for API calls
- **Pytest** - Testing framework
- **python-dotenv** - Environment variable management
- **OpenWeather API** - Weather data provider

## Project Structure

```
capstone-project-1/
├── data/
│   ├── raw/
│   │   └── worldcities.csv
│   └── processed/
│       └── merged_data.csv
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── transformer.py
│   ├── pipeline.py
│   └── app.py
├── tests/
│   ├── test_cleaner.py
│   └── test_transformer.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenWeather API key ([Get one here](https://openweathermap.org/api))

### Installation

1. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

> **Note**: The `.env` file is git-ignored for security.

### Running the Pipeline

Execute the data pipeline before starting the API:

```bash
python -m src.pipeline
```

**Pipeline workflow:**
1. Loads city data from CSV
2. Cleans nulls and duplicates
3. Fetches weather data from OpenWeather API
4. Adds derived insights (temperature categories, population buckets)
5. Saves processed data to `data/processed/merged_data.csv`

### Starting the API Server

```bash
uvicorn src.app:app --reload
```

Access the interactive API documentation at: **http://127.0.0.1:8000/docs**

## API Endpoints

### Get All Cities
```http
GET /cities?page=1&limit=10
```
Returns paginated list of cities with weather data.

**Query Parameters:**
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10)

### Get Cities by Temperature Category
```http
GET /cities/by-temperature?category=Warm
```
Filters cities by temperature range using dropdown selection.

**Temperature Categories:**
| Category | Range |
|----------|-------|
| Freezing | < 0°C |
| Cold | 0–10°C |
| Mild | 10–20°C |
| Warm | 20–30°C |
| Hot | > 30°C |

Returns `404` if no cities exist for the selected category.

### Get Specific City
```http
GET /cities/{city_name}
```

**Example:**
```http
GET /cities/delhi
```

### Comparative Insights
```http
GET /insights/comparative-view
```

Returns dataset-wide analytics:
- Average temperature and population
- Warmest and coldest cities
- Most and least populated cities

> **Note**: All insights are relative to the available dataset, not global rankings.

## Data Classification

### Population Buckets

| Bucket | Population Range |
|--------|-----------------|
| Small | < 1M |
| Medium | 1M – 5M |
| Large | 5M – 10M |
| Mega | > 10M |

## Testing

Run the test suite:

```bash
pytest
```

**Test coverage includes:**
- Data cleaning logic
- Temperature categorization
- Population bucketing
- Edge cases and boundary conditions

All tests pass successfully.

## Design Principles

- **Modular Architecture**: Clean separation of concerns across modules
- **Absolute Imports**: Uses `src` package layout for clarity
- **Secure Configuration**: Environment variables handled via `.env`
- **Clear Error Handling**: Meaningful success and error messages
- **Honest Analytics**: Insights scoped to available data coverage
- **RESTful Design**: Follows REST API best practices

## Configuration

The project uses `pytest.ini` for test configuration and clean import resolution:

```ini
[pytest]
pythonpath = .
```
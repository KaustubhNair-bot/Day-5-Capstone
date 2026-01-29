# Day 5 Capstone – Data Processing & Analytics Service

## Project Overview
This project implements an end-to-end data processing and analytics service.
It ingests real-time weather data from the OpenWeatherMap API and combines it
with city demographic data from a CSV dataset. The data is cleaned, transformed,
and exposed through REST APIs for easy consumption.

The project demonstrates real-world concepts such as API integration,
data cleaning, transformation, modular pipeline design, testing, and API development.

---

## What Is Implemented
- Weather data ingestion using OpenWeatherMap API
- CSV data loading and filtering using Pandas
- Data cleaning (null handling, duplicates, normalization)
- Data transformation and feature engineering
- Modular ETL pipeline execution
- REST APIs using FastAPI
- Unit tests using Pytest
- Structured logging for observability

---

## Setup Instructions

### 1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a .env file in the project root:
```bash
OPENWEATHER_API_KEY=your_api_key_here
```

### Run the Data Pipeline
This step fetches weather data, processes it, and generates the final dataset.
```bash
python src/pipeline.py
```

Output:
```bash
data/processed/merged_data.csv
```

### Run the API Server
```bash
uvicorn src.app:app --reload
```

Swagger UI:
```bash
http://127.0.0.1:8000/docs
```

## API Usage Examples
### Get all cities
```bash
GET /cities
```

### Get city by name
```bash
GET /cities/{city_name}
```

Example:
```bash
GET /cities/tokyo
```

### Get cities by temperature category
```bash
GET /cities/temp_category/{category}
```
Example:
```bash
GET /cities/temp_category/Hot
```

## Run Unit Tests
```bash
pytest
```
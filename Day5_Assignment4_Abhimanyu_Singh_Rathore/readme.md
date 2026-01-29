# City Weather Analytics API

##  Project Overview

This project is a **Data Processing & Analytics Service** built using Python and FastAPI.  
It demonstrates how to ingest real-world data from multiple sources, clean and transform it, and expose useful insights through REST APIs.

The application:
- Reads real city data from a CSV file
- Fetches real-time weather data from an external API
- Cleans and transforms the combined data
- Exposes the processed data through REST endpoints
- Includes unit tests for core business logic

---

##  Data Sources

### CSV Dataset
- **Source:** SimpleMaps – World Cities Dataset
- **File:** `worldcities.csv`
- **Fields used:**
  - city
  - country
  - latitude
  - longitude
  - population

###  External API
- **API:** OpenWeatherMap Current Weather API
- **Data fetched:**
  - Temperature
  - Humidity
  - Weather condition

---

## Project Structure
day5-capstone/
├── src/
│ ├── app.py # FastAPI application
│ ├── config.py # Configuration values
│ ├── api_client.py # External API calls
│ ├── data_loader.py # CSV loading logic
│ ├── data_cleaner.py # Data cleaning logic
│ └── transformer.py # Data transformation logic
│
├── data/
│ └── raw/
│ └── worldcities.csv
│
├── tests/
│ ├── test_cleaner.py
│ └── test_transformer.py
│
├── requirements.txt
├── README.md
└── .gitignore
##  How the Application Works

1. **Application Startup**
   - Load city data from CSV
   - Clean and normalize the dataset
   - Filter cities by minimum population
   - Select top cities by population
   - Fetch real-time weather data
   - Create a final enriched dataset
   - Store processed data in memory

2. **API Requests**
   - All API endpoints serve data directly from memory
   - No repeated CSV reads or API calls per request


### Get all cities

API Endpoints 
GET /cities


Returns weather data for all processed cities.


###  Get a specific city


GET /cities/{city_name}

Returns weather data for a single city.

Example:


GET /cities/delhi

### GET /cities/filter?temp_category=Hot


Valid categories:
- Cold
- Moderate
- Hot




##  Unit Testing

Unit tests are written using **pytest** and focus on core business logic.

### Tested Components:
- Data cleaning logic
- Temperature category transformation logic

### Run tests:
```bash
pytest


All tests must pass before submission.

🛠 Setup Instructions
 Clone the repository
git clone <repository-url>
cd day5-capstone

 Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

 Install dependencies
pip install -r requirements.txt

 Add API key

Update API_KEY in src/config.py with your OpenWeather API key.

 Run the application
uvicorn src.app:app --reload


Access API at:

http://127.0.0.1:8000

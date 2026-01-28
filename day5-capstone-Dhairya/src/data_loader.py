import pandas as pd 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "worldcities.csv"


def load_city_data(country:str,min_population:int=1000000) -> pd.DataFrame:
    """
    Load city data from CSV and filter by country and minimum population.
    """
    df = pd.read_csv(DATA_PATH)

    required_columns = ["city", "lat", "lng", "country", "population"]
    df = df[required_columns]

    df = df[df['population'] >= min_population]

    if country:
        df = df[df["country"].str.lower() == country.lower()]

    return df

def prepare_city_payload(df:pd.DataFrame,limit:int=5) ->list:
    """
    Prepare city payload for API requests.
    """
    cities = []

    for _, row in df.head(limit).iterrows():
        city_info = {
            "city": row["city"],
            "lat": row["lat"],
            "lng": row["lng"]
        }

        cities.append(city_info)

    return cities

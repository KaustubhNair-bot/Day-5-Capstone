#standardize column and city names and remove duplicates and unusable rows

import pandas as pd

def clean_city_table(city_table: pd.DataFrame) -> pd.DataFrame:

    cleaned_table = city_table.copy()

    cleaned_table.columns = [col.strip().lower() for col in cleaned_table.columns] 

    cleaned_table["city"] = cleaned_table["city"].str.strip().str.lower() 

    cleaned_table = cleaned_table.dropna(subset=["lat","lng"]) #removes rows with unusable lat/lng or either missing

    cleaned_table = cleaned_table.drop_duplicates(subset=["city","country"]) #removes duplicate city-country pairs uses them as a uniqueness key

    return cleaned_table

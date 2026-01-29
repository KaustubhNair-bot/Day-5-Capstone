# add derived columns to a DataFrame; converting raw numbers to categorical labels

import pandas as pd

def categorize_temperature(celsius):
    if celsius is None:
        return "Unknown"
    
    if celsius < 0:
        return "Freezing"
    elif 0 <= celsius < 10:
        return "Cold"
    elif 10 <= celsius < 20:
        return "Mild"
    elif 20 <= celsius < 30:
        return "Warm"
    else:
        return "Hot"
    
def bucket_population(population):
    if population is None:
        return "Unknown"
    
    if population < 1_000_000:
        return "Small"
    elif 1_000_000 <= population < 5_000_000:
        return "Medium"
    elif 5_000_000 <= population < 10_000_000:
        return "Large"
    else:
        return "Mega"

def transform_city_data(merged_table: pd.DataFrame) -> pd.DataFrame:

    transformed_table = merged_table.copy()

    transformed_table["temp_category"] = transformed_table["temp"].apply(categorize_temperature)
    transformed_table["population_bucket"] = transformed_table["population"].apply(bucket_population)

    return transformed_table

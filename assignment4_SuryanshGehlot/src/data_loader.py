# only reads csv, filter rows and returns a DataFrame

import pandas as pd

COLUMNS_NEEDED = ["city","country","lat","lng","population"]

def load_city_table(csv_path:str,min_pop: int = 1000000) -> pd.DataFrame: #type hint; can be removed

    city_table = pd.read_csv(csv_path) #reading csv

    city_table = city_table[COLUMNS_NEEDED] #data minimization

    city_table = city_table[city_table["population"] > min_pop] #filtering

    return city_table

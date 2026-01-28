import pandas as pd


class CityDataLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.csv_path)

    def filter_by_country_and_population(
        self,
        df: pd.DataFrame,
        country: str,
        min_population: int = 1_000_000
    ) -> pd.DataFrame:
        filtered_df = df[
            (df["country"] == country) &
            (df["population"] >= min_population)
        ]
        return filtered_df

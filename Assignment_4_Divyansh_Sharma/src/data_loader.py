import pandas as pd


class DataLoader:
    def __init__(self, file_path="data/raw/worldcities.csv"):
        self.file_path = file_path

    def load_cities(self):
        try:
            df = pd.read_csv(self.file_path)
            # Filtering for population > 1 million
            return df[df["population"] > 1000000]

        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

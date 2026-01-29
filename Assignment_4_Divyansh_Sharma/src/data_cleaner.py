class DataCleaner:
    def clean(self, df):
        # Cleans the basic city dataframe: handles casing, null and duplicates.
        if df is None:
            return None

        # Working on a copy
        df = df.copy()
        # Standardize city and country names to lowercase
        df["city"] = df["city"].str.lower()
        df["country"] = df["country"].str.lower()
        # drop row which have no important information
        df = df.dropna(subset=["lat", "lng", "population"])
        # Removing of any duplicate city entries
        df = df.drop_duplicates(subset=["city", "country"])

        return df

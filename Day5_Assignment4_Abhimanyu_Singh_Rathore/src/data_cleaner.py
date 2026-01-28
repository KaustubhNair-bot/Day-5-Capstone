

import pandas as pd


# Custom exception class for data cleaning errors.
class DataCleanError(Exception):
    pass


def clean_city_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw city DataFrame by:
    - Normalizing column names
    - Standardizing city names
    - Removing invalid and duplicate rows

    Parameters:
        df (pd.DataFrame): Raw city data loaded from CSV

    Returns:
        pd.DataFrame: Cleaned and validated city data
    """
    try:
        # Convert all column names to lowercase.
        # This avoids bugs caused by inconsistent casing
        # (e.g., 'City' vs 'city').
        df.columns = df.columns.str.lower()

        # Convert city names to lowercase so comparisons
        # and joins behave consistently across the dataset.
        df["city"] = df["city"].str.lower()

        # Drop rows that are missing critical fields.
        # Without these fields, the city record cannot be used
        df = df.dropna(subset=["city", "country", "lat", "lng", "population"])

        # Remove duplicate city entries.
        # A city is considered duplicate if the same city and country
        # appear more than once.
        df = df.drop_duplicates(subset=["city", "country"])

        # Return the cleaned DataFrame so it can be reused
        # by the transformation and API layers.
        return df

    except KeyError as e:
        # Raised when an expected column (like 'city' or 'lat')
        # does not exist in the input DataFrame.
        raise DataCleanError(f"Missing expected column during cleaning: {e}")

    except Exception as e:
        # Catch-all for any unexpected issues during cleaning.
        # Wrapping it in DataCleanError keeps error handling consistent.
        raise DataCleanError(f"Data cleaning failed: {str(e)}")

import pandas as pd

def clean_city_data(df):
    
    # Normalise column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()

    # Normalize city and country names
    if "city" in df.columns:
        df["city"] = df["city"].str.lower().str.strip()
    if "country" in df.columns:
        df["country"] = df["country"].str.lower().str.strip()

    # Drop rows with missing lat/lng just in case
    df = df.dropna(subset=["lat", "lng"])

    # Remove duplicates based on city and country
    df = df.drop_duplicates(subset=["city", "country"])

    # Reset index after cleaning
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/raw/worldcities.csv")
    df = clean_city_data(df)
    print(df.head())
    print(f"Total cities after cleaning: {len(df)}")
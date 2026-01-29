import pandas as pd

def load_cities(file_path="data/raw/worldcities.csv"):
    
    # Load CSV
    df = pd.read_csv(file_path)

    # Keep relevant columns
    df = df[['city','country','lat','lng','population']]

    # Filter cities by population greater than 1 million
    df = df[df["population"] > 1_000_000]
   
   # Drop rows with missing crucial data to handle missing data
    df = df.dropna(subset=["city", "country", "lat", "lng", "population"])

    return df


if __name__ == "__main__":
    df = load_cities()
    print(df.head())
    print(f"Total cities loaded: {len(df)}")
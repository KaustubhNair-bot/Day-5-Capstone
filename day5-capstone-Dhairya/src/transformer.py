import pandas as pd
from pathlib import Path


def temperature_category(temp_celsius: float) -> str:
    """
    Categorize temperature into Cold / Moderate / Hot.
    """
    if temp_celsius < 15:
        return "Cold"
    elif 15 <= temp_celsius <= 30:
        return "Moderate"
    else:
        return "Hot"


def population_bucket(population: int) -> str:
    """
    Categorize population into Small / Medium / Large.
    """
    if population < 2_000_000:
        return "Small"
    elif 2_000_000 <= population <= 10_000_000:
        return "Medium"
    else:
        return "Large"


def merge_city_weather_data(
    city_df: pd.DataFrame,
    weather_data: list
) -> pd.DataFrame:
    """
    Merge cleaned city data with weather data and create derived columns.
    """
    # Convert weather list to DataFrame
    weather_df = pd.DataFrame(weather_data)

    # Merge on city name (INNER JOIN)
    merged_df = pd.merge(
        weather_df,
        city_df,
        on="city",
        how="inner"
    )

    # Create derived columns
    merged_df["temp_category"] = merged_df["temperature"].apply(temperature_category)
    merged_df["population_bucket"] = merged_df["population"].apply(population_bucket)

    return merged_df


def save_final_dataset(df: pd.DataFrame) -> None:
    """
    Save final merged dataset as CSV.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    output_dir = BASE_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "merged_data.csv"
    df.to_csv(output_path, index=False)

    print(f"[INFO] Final dataset saved at {output_path}")

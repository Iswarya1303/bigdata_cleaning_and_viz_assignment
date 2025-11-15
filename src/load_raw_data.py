import pandas as pd
from pathlib import Path


csv_path = Path(__file__).resolve().parents[1] / "data" / "stock_market.csv"

def main():
    # Load the raw CSV file
    df = pd.read_csv(csv_path)

    print(" --- RAW DATA SUMMARY --- \n")

    # 1. Shape
    print("1) Shape:", df.shape)

    # 2. Show first few rows
    print("\n2) Preview of the data:")
    print(df.head())

    # 3. Schema
    print("\n3) Column data types:")
    print(df.dtypes)

    # 4. null summary
    print("\n4) Null Summary:")
    print(df.isna().sum())

if __name__ == "__main__":
    main()







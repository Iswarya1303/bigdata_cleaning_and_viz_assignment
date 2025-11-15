import pandas as pd
from pathlib import Path

# Paths
data_dir = Path(__file__).resolve().parents[1] / "data"
cleaned_path = data_dir / "cleaned.parquet"

agg1_path = data_dir / "agg1.parquet"
agg2_path = data_dir / "agg2.parquet"
agg3_path = data_dir / "agg3.parquet"

def main():
    # Load cleaned data
    df = pd.read_parquet(cleaned_path)

    
    # Aggregation 1: Daily avg close price by ticker
    
    agg1 = (
        df.groupby(["trade_date", "ticker"], as_index=False)["close_price"]
          .mean()
          .rename(columns={"close_price": "avg_close_price"})
    )
    agg1.to_parquet(agg1_path, index=False)

    
    # Aggregation 2: Avg volume by sector
    
    agg2 = (
        df.groupby("sector", as_index=False)["volume"]
          .mean()
          .rename(columns={"volume": "avg_volume"})
    )
    agg2.to_parquet(agg2_path, index=False)

    # Aggregation 3: Daily return by ticker
    
    df_sorted = df.sort_values(["ticker", "trade_date"])
    df_sorted["daily_return"] = df_sorted.groupby("ticker")["close_price"].pct_change()

    agg3 = df_sorted[["trade_date", "ticker", "close_price", "daily_return"]]
    agg3.to_parquet(agg3_path, index=False)

    print(" Aggregations created successfully:")
    print(" -", agg1_path)
    print(" -", agg2_path)
    print(" -", agg3_path)

if __name__ == "__main__":
    main()

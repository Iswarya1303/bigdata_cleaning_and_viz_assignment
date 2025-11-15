import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parents[1] / "data" / "stock_market.csv"
cleaned_path = Path(__file__).resolve().parents[1] / "data" / "cleaned.parquet"

def main():
    df = pd.read_csv(csv_path)

    # 1) Headers -> snake_case
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2) Trim whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # 3) Standardize obvious missing values to one value (NaN)
    missing_values = {"", "NA", "N/A", "na", "n/a", "null", "Null", "-"}
    for col in str_cols:
        df[col] = df[col].replace(missing_values, pd.NA)

    # 4) Parse date column -> datetime 
    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        format="%m/%d/%Y",
        errors="coerce"
    )

    # 5) Define target schema for numeric columns
    #    open_price, close_price -> float
    #    volume -> nullable integer
    df["open_price"] = pd.to_numeric(df["open_price"], errors="coerce")
    df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    # 6) Define target schema for boolean column "validated"
    #    yes/y -> True, no/n -> False, everything else -> <NA>
    validated_str = df["validated"].astype("string").str.strip().str.lower()
    df["validated"] = pd.NA
    df.loc[validated_str.isin(["yes", "y"]), "validated"] = True
    df.loc[validated_str.isin(["no", "n"]), "validated"] = False
    df["validated"] = df["validated"].astype("boolean")

    # Ensure other columns are strings
    df["ticker"] = df["ticker"].astype("string")
    df["sector"] = df["sector"].astype("string")
    df["currency"] = df["currency"].astype("string")
    df["exchange"] = df["exchange"].astype("string")
    df["notes"] = df["notes"].astype("string")

    # 7) Deduplicate rows if any
    df = df.drop_duplicates()

    # 8) Save to cleaned.parquet
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cleaned_path, index=False)

    print("Cleaned file created:", cleaned_path)
    print("Shape:", df.shape)
    print("\nDtypes:")
    print(df.dtypes)

if __name__ == "__main__":
    main()

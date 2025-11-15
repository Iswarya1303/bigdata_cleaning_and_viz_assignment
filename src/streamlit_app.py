import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- Paths ----------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
AGG1_PATH = DATA_DIR / "agg1.parquet"  # daily avg close by ticker
AGG2_PATH = DATA_DIR / "agg2.parquet"  # avg volume by sector
AGG3_PATH = DATA_DIR / "agg3.parquet"  # daily return by ticker


# ---------- Data loading helpers ----------

@st.cache_data
def load_parquet(path: Path) -> pd.DataFrame:
    """Load a parquet file into a DataFrame (cached for speed)."""
    return pd.read_parquet(path)


def main():
    st.title("Stock Market – Cleaning & Viz Assignment")
    st.write(
        "This dashboard loads **aggregated parquet files** and lets you "
        "explore stock behavior by ticker and date range."
    )

    # Load aggregated data
    agg1 = load_parquet(AGG1_PATH)  # trade_date, ticker, avg_close_price
    agg2 = load_parquet(AGG2_PATH)  # sector, avg_volume
    agg3 = load_parquet(AGG3_PATH)  # trade_date, ticker, close_price, daily_return

    # Making sure trade_date is datetime 
    agg1["trade_date"] = pd.to_datetime(agg1["trade_date"])
    agg3["trade_date"] = pd.to_datetime(agg3["trade_date"])

    # ---------- Sidebar Filters ----------
    st.sidebar.header("Filters")

    # Ticker filter (from agg1 / agg3)
    tickers = sorted(agg1["ticker"].dropna().unique().tolist())
    selected_ticker = st.sidebar.selectbox("Select ticker", tickers)

    # Date range filter (based on agg1 for that ticker)
    ticker_dates = agg1.loc[agg1["ticker"] == selected_ticker, "trade_date"]
    min_date = ticker_dates.min()
    max_date = ticker_dates.max()

    start_date, end_date = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Ensure start_date <= end_date
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")
        return

    # Convert to Timestamp for filtering
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date)

    # ---------- Filtered Data ----------
    # Filter agg1 for price chart
    agg1_filtered = agg1[
        (agg1["ticker"] == selected_ticker)
        & (agg1["trade_date"] >= start_ts)
        & (agg1["trade_date"] <= end_ts)
    ]

    # Filter agg3 for daily return chart
    agg3_filtered = agg3[
        (agg3["ticker"] == selected_ticker)
        & (agg3["trade_date"] >= start_ts)
        & (agg3["trade_date"] <= end_ts)
    ]

    # ---------- Layout ----------
    st.subheader(f"Daily Average Close Price – {selected_ticker}")
    if agg1_filtered.empty:
        st.warning("No data for this ticker and date range.")
    else:
        st.line_chart(
            agg1_filtered.set_index("trade_date")["avg_close_price"],
            use_container_width=True,
        )

    st.subheader(f"Daily Return – {selected_ticker}")
    if agg3_filtered.empty:
        st.warning("No return data for this ticker and date range.")
    else:
        st.line_chart(
            agg3_filtered.set_index("trade_date")["daily_return"],
            use_container_width=True,
        )

    st.subheader("Average Volume by Sector")
    if agg2.empty:
        st.warning("No sector volume data available.")
    else:
        st.bar_chart(
            agg2.set_index("sector")["avg_volume"],
            use_container_width=True,
        )

    # ---------- Data Preview ----------
    st.markdown("### Data Preview")
    with st.expander("Show raw aggregated data"):
        st.write("agg1  Daily average close by ticker")
        st.dataframe(agg1.head(20))

        st.write("agg2 Average volume by sector")
        st.dataframe(agg2.head(20))

        st.write("agg3 Daily return by ticker")
        st.dataframe(agg3.head(20))


if __name__ == "__main__":
    main()

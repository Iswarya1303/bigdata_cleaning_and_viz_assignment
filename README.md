# Cleaning and Visualization – Stock Market Dataset

This assignment follows the requirements of the “Cleaning and Viz” assignment for the Big Data Tools and Techniques course. The work is organized into four stages: raw data review, data cleaning and schema normalization, creation of aggregations, and final visualization using Streamlit.

---

## 1. Raw Data Review

The assignment begins by loading the raw CSV file and performing an initial inspection.  
The following information was obtained as required:

- Number of rows and columns  
- Preview of the first few records  
- Basic data types of each column  
- Summary of missing or null values  

This provides an understanding of the dataset before any transformations.

---

## 2. Data Cleaning and Schema Normalization

The dataset was standardized according to the assignment instructions.  
The following steps were completed:

- Converted column names to snake_case  
- Removed unnecessary spaces from all text fields  
- Standardized multiple representations of missing values into a single null format  
- Reformatted dates into the required `YYYY-MM-DD` format  
- Applied a consistent schema (dates, floats, ints, strings, booleans)  
- Removed duplicate rows  
- Saved the cleaned dataset in Parquet format  

The result is a clean, uniform dataset ready for analysis.

---

## 3. Aggregations

As required, simple aggregations were generated from the cleaned dataset and saved as separate Parquet files.  
The following summaries were created:

- Daily average closing price grouped by ticker  
- Average trading volume grouped by sector  
- Daily return (percentage change) calculated per ticker  

These aggregated files are used directly in the visualization step.

---

## 4. Streamlit Visualization

A Streamlit dashboard was built to visualize the cleaned and aggregated data.  
The application includes:

- Ticker selection  
- Date-range filtering  
- Line chart of daily average closing price  
- Line chart showing daily returns  
- Bar chart of average trading volume by sector  

The dashboard provides an interactive way to explore the dataset and observe trends.

Screenshots of the running application are included in the `screenshots` folder, as required by the assignment.

---

## Tools Used

- Python  
- Pandas  
- Parquet / PyArrow  
- Streamlit  
- UV and VS Code  

---

## Summary

This project completes all steps outlined in the assignment:  
raw data inspection, data cleaning, creation of aggregations, and interactive visualization, along with the required screenshots.

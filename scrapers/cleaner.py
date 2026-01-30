import csv
import pandas as pd


titles = [
    "Data Engineer",
    "Junior Data Engineer",
    "Senior Data Engineer",
    "Lead Data Engineer",
    "Principal Data Engineer",
    "Data Platform Engineer",
    "Big Data Engineer",
    "Analytics Engineer",
    "ETL Engineer",
    "Data Infrastructure Engineer"
]


def data_cleaner(input_csv, output_csv,write_mode):
    df = pd.read_csv(input_csv)
    final_df = df[
    df["job_title"]
    .astype(str)
    .str.lower()
    .str.contains(r"\bdata\s+engin(eer|er|ner|nier|inner)?\b", regex=True, na=False)][["company", "job_title", "location", "job_url"]]

    final_df.to_csv(output_csv, mode=write_mode, index=False)
    print(f"Cleaned data saved to {output_csv}")
import subprocess
import pandas as pd
from dagster import asset, Output, MetadataValue

SCRAPY_PROJECT_DIR = "../pc_scrape"
WINDNET_CSV = f"{SCRAPY_PROJECT_DIR}/windnetpc.csv"
EASYPC_CSV = f"{SCRAPY_PROJECT_DIR}/easypc.csv"
FINAL_OUTPUT = "final_scraped_data.csv"

@asset
def scrape_windnetpc() -> Output[pd.DataFrame]:
    subprocess.run(
        ["scrapy", "crawl", "windnetpc", "-o", "windnetpc.csv", "-t", "csv"],
        check=True,
        cwd=SCRAPY_PROJECT_DIR
    )
    df = pd.read_csv(WINDNET_CSV)
    return Output(
        df,
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@asset
def scrape_easypc() -> Output[pd.DataFrame]:
    subprocess.run(
        ["scrapy", "crawl", "easypc", "-o", "easypc.csv", "-t", "csv"],
        check=True,
        cwd=SCRAPY_PROJECT_DIR
    )
    df = pd.read_csv(EASYPC_CSV)
    return Output(
        df,
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@asset
def validate_data(scrape_windnetpc: pd.DataFrame, scrape_easypc: pd.DataFrame) -> None:
    for name, df in [("windnetpc", scrape_windnetpc), ("easypc", scrape_easypc)]:
        if df["product"].isnull().any() or df["price"].isnull().any():
            raise ValueError(f"{name} contains null values in 'product' or 'price'")
        if df.empty:
            raise ValueError(f"{name} produced an empty dataset")

@asset
def processed_data(scrape_windnetpc: pd.DataFrame, scrape_easypc: pd.DataFrame) -> Output[pd.DataFrame]:
    df = pd.concat([scrape_windnetpc, scrape_easypc], ignore_index=True)
    df.drop_duplicates(inplace=True)
    df = df.reset_index(drop=True)
    return Output(
        df,
        metadata={
            "total_records": len(df),
            "columns": list(df.columns)
        }
    )

@asset
def save_to_csv(processed_data: pd.DataFrame) -> None:
    processed_data.to_csv(FINAL_OUTPUT, index=False)
    print(f"Saved combined data to {FINAL_OUTPUT}")
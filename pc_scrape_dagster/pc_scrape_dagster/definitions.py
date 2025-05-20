from dagster import Definitions, define_asset_job, ScheduleDefinition, load_assets_from_modules
from . import assets  # this refers to your assets.py (we’ll create assets there)

# Load assets from assets.py
all_assets = load_assets_from_modules([assets])

# Create a job to run all assets
daily_job = define_asset_job("daily_scrape_job", selection="*")

# Schedule: run every day at 9 AM
daily_schedule = ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 9 * * *",
)

# Definitions object to expose to Dagster
defs = Definitions(
    assets=all_assets,
    jobs=[daily_job],
    schedules=[daily_schedule],
)
from typing import Literal, List, Dict, Tuple
from database.db import generate_db_instance
from etl.extract import extract_afl_from_sheet, AFL_YEARS
from etl.transform import transform_sheet_data
from etl.load import load_to_db
from database.models.raw import RawFlightLog

# from database.models.analytics
from local_types.data_type import AflDataType, RawAflDbType
from utils.db import db_comparison_data, truncate_db

from prefect import flow, task
from prefect.variables import Variable
# from prefect.logging import get_run_logger

import os


@task
def setup_database(
    db_creds_name: str,
    db_type: Literal["postgres", "mysql"],
):
    """Setup database"""
    db_cred = Variable.get(db_creds_name)
    RawFlightLog._meta.table_name = db_cred["table"]
    RawFlightLog._meta.schema = db_cred["schema"]
    db = generate_db_instance(db_cred, db_type)
    RawFlightLog.bind_database(db)
    return db


@task
def extract_data(year: AFL_YEARS):
    """Extract data from sheet"""
    return extract_afl_from_sheet(year)


@task
def get_db_info(year: int) -> Tuple[int | None, int]:
    """Get database comparison data"""
    return db_comparison_data(year)


@task(log_prints=True)
def filter_new_records(sheet_data: List[Dict], db_last_id: int) -> List[Dict]:
    """Filter for new records"""
    # logger = get_run_logger()
    filtered_data = [data for data in sheet_data if data["id"] > db_last_id]
    # logger.debug(filtered_data[0:10])
    # print(filtered_data[0:10])
    return filtered_data


@task(log_prints=True)
def transform_data(sheet_data: List[AflDataType], year: AFL_YEARS):
    """Transform sheet data"""
    return transform_sheet_data(sheet_data, year)


@task(log_prints=True)
def load_data(sheet_data: List[RawAflDbType]) -> None:
    """Load data to database"""
    load_to_db(sheet_data)


@flow(name="AFL ETL Pipeline", log_prints=True, retries=3, retry_delay_seconds=5)
def main_pipeline(
    year: str,
    db_creds_name: str,
    db_type: Literal["postgres", "mysql"],
    truncate: bool = False,
) -> None:
    """
    Main ETL pipeline for processing flight log data.
    """
    print(f"Running ETL pipeline for year {year} with DB type {db_type}")
    # Database setup
    setup_database(db_creds_name, db_type)

    # Extract data
    sheet_data = extract_data(year)

    if not sheet_data:
        raise ValueError(f"No sheet data found for year {year}")

    if truncate:
        truncate_db(int(year))
        print(f"Database truncated for year {year}.")
    else:
        sheet_data_last_id = sheet_data[-1]["id"]
        db_last_id, db_data_count = get_db_info(int(year))
        print(f"Database last ID: {db_last_id}, Database record count: {db_data_count}")

        # Validate database state
        if db_last_id == 0:
            raise ValueError(f"Empty database for year {year}. Check connection.")

        if db_last_id is not None:
            # Check for new data
            if sheet_data_last_id <= db_last_id:
                print(f"No new data to load for year {year}.")
                return

            # Filter and process new records
            if sheet_data_last_id > db_last_id:
                sheet_data = filter_new_records(sheet_data, db_last_id)

            # Handle data count mismatch
            if sheet_data_last_id == db_last_id and len(sheet_data) != db_data_count:
                truncate_db(int(year))

        # Transform and load
    transformed_data = transform_data(sheet_data, year)
    # print(transformed_data)
    load_data(transformed_data)
    return


# # LOCAL ONLY
# rerun_years = [
#     # "2016",
#     # "2017",
#     # "2018",
#     # "2019",
#     "2020",
#     "2021",
#     "2022",
#     "2023",
#     "2024",
# ]

# for year in rerun_years:
#     main_pipeline(
#         year=year,
#         db_creds_name="local_afl_postgres",
#         db_type="postgres",
#         truncate=True,
#     )


if __name__ == "__main__":
    DEPLOY_NAME = os.getenv("DEPLOY_NAME", "afl_pipeline")
    main_pipeline.serve(
        name=DEPLOY_NAME,
        tags=["afl"],
        # parameters={
        #     "year": "2025",
        #     "db_creds_name": "local_afl_postgres",
        #     "db_type": "postgres",
        # },
        # cron="0 0 * * *",
    )

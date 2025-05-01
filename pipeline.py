from typing import Literal, List, Dict, Tuple
from database.db import generate_db_instance
from etl.extract import extract_afl_from_sheet, AFL_YEARS
from etl.transform import transform_sheet_data
from etl.load import load_to_db
from database.models import TestFlightLog
from utils.db import db_comparison_data, truncate_db

from prefect import flow, task
# from prefect.logging import get_run_logger


@task
def setup_database(db_creds_name: str, db_type: Literal["postgres", "mysql"]):
    """Setup database connection"""
    db = generate_db_instance(db_creds_name, db_type)
    TestFlightLog.bind_database(db)
    return db


@task
def extract_data(year: AFL_YEARS) -> List[Dict]:
    """Extract data from sheet"""
    return extract_afl_from_sheet(year)


@task
def get_db_info(year: int) -> Tuple[int, int]:
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
def transform_data(sheet_data: List[Dict], year: AFL_YEARS) -> List[Dict]:
    """Transform sheet data"""
    # logger = get_run_logger()
    # logger.debug(sheet_data[0:10])
    # print(sheet_data[0:10])
    return transform_sheet_data(sheet_data, year)


@task(log_prints=True)
def load_data(sheet_data: List[Dict]) -> None:
    """Load data to database"""
    # print(sheet_data[0:5])
    load_to_db(sheet_data)


@flow(name="AFL ETL Pipeline", log_prints=True)
def main_pipeline(
    year: AFL_YEARS, db_creds_name: str, db_type: Literal["postgres", "mysql"]
) -> None:
    """
    Main ETL pipeline for processing flight log data.
    """
    print(f"Running ETL pipeline for year {year} with DB type {db_type}")
    # Database setup
    setup_database(db_creds_name, db_type)

    # Extract data
    sheet_data = extract_data(year)
    sheet_data_last_id = sheet_data[-1]["id"]
    db_last_id, db_data_count = get_db_info(int(year))

    # Validate database state
    if db_last_id == 0:
        raise ValueError(f"Empty database for year {year}. Check connection.")

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


if __name__ == "__main__":
    # main_pipeline.serve(
    #     name="test_afl_pipeline",
    #     tags=["afl", "test"],
    #     parameters={
    #         "year": "2025",
    #         "db_creds_name": "local_test_postgres_credentials",
    #         "db_type": "postgres",
    #     },
    #     cron="0 0 * * *",
    # )
    main_pipeline.from_source(
        source="https://github.com/analyst-susiair/prefect-test.git",
        entrypoint="pipeline.py:main_pipeline",
    ).deploy(  # type: ignore[no-untyped-call]
        name="deployed_test_afl_pipeline",
        tags=["afl", "etl", "test"],
        work_pool_name="main_workpool",
        # push=False,
        # image="ghcr.io/your-docker-image:latest",
        parameters={
            "year": "2025",
            "db_creds_name": "local_test_postgres_credentials",
            "db_type": "postgres",
        },
        cron="0 0 * * *",
        job_variables={
            "pip_packages": [
                "google-auth",
                "gspread-asyncio",
                "peewee>=3.17.9",
                "psycopg2>=2.9.10",
            ]
        },
    )
    # (
    #     year="2025",
    #     db_creds_name="local_test_postgres_credentials",
    #     db_type="postgres",
    # )

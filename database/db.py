from typing import Literal
from peewee import PostgresqlDatabase, MySQLDatabase
from prefect.variables import Variable


# db_creds = Variable.get("local_test_postgres_credentials")


def generate_db_instance(
    # db_creds_name: str = "local_test_postgres_credentials",
    db_creds: any,
    db_type: Literal["postgres", "mysql"] = "postgres",
) -> PostgresqlDatabase:
    # DATABASE_URL = "postgresql://postgres:eLtRvifcb9CtfTq6Azd7WCgfdZB0f0wkwXxGPdGBabYT1qDyTgM3rRWvapnsyWnJ@192.168.0.170:5431/afl-dev"
    # db_creds = Variable.get(db_creds_name)

    if db_type == "postgres":
        db = PostgresqlDatabase(
            database=db_creds["database"],  # type: ignore
            user=db_creds["user"],  # type: ignore
            password=db_creds["password"],  # type: ignore
            host=db_creds["host"],  # type: ignore
            port=db_creds["port"],  # type: ignore
        )
    elif db_type == "mysql":
        db = MySQLDatabase(
            database=db_creds["database"],  # type: ignore
            user=db_creds["user"],  # type: ignore
            password=db_creds["password"],  # type: ignore
            host=db_creds["host"],  # type: ignore
            port=db_creds["port"],  # type: ignore
        )

    # db.connect()
    return db


# db = postgres_db()

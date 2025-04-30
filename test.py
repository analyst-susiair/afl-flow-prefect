from typing import List
from prefect import flow, task
# from prefect.server import


@task
def extract():
    data = ["This", "is", "running", "from", "prefect"]
    return data


@task
def transform(data: List[str]):
    transformed_data = str()

    return transformed_data


@task(log_prints=True)
def load(data: List[dict[str, int]]):
    print(data)


@flow
def main():
    e = extract()
    t = transform(e)
    load(t)


if __name__ == "__main__":
    # main.serve(name="ETL Test Flow", tags=["etl", "test"], interval=30)
    main.from_source(
        source="https://github.com/analyst-susiair/prefect-test.git",
        entrypoint="test.py:main",
    ).deploy(
        name="prefect-test-flow",
        work_pool_name="main_workpool",
        tags=["test"],
        cron="0 * * * *",
    )

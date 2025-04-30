from database.models import TestFlightLog


def db_comparison_data(year: int) -> tuple[int, int]:
    last_id = (
        TestFlightLog.select()
        .where(TestFlightLog.year == year)
        .order_by(TestFlightLog.id.desc())
        .get()
        .id
    )
    data_count = TestFlightLog.select().where(TestFlightLog.year == year).count()

    return last_id, data_count


def truncate_db(year: int) -> None:
    """
    Truncate the database table for the given year.
    """
    TestFlightLog.delete().where(TestFlightLog.year == year).execute()

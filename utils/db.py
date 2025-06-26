from database.models.raw import RawFlightLog


def db_comparison_data(year: int) -> tuple[int | None, int]:
    last_id = (
        RawFlightLog.select()
        .where(RawFlightLog.year == year)
        .order_by(RawFlightLog.id.desc())
        .get_or_none()
    )
    if last_id is not None:
        last_id = last_id.id
    else:
        last_id = None
    data_count = RawFlightLog.select().where(RawFlightLog.year == year).count()

    return last_id, data_count


def truncate_db(year: int) -> None:
    """
    Truncate the database table for the given year.
    """
    RawFlightLog.delete().where(RawFlightLog.year == year).execute()

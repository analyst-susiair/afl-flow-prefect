from typing import List
from database.models.raw import RawFlightLog
from local_types.data_type import RawAflDbType


def load_to_db(data: List[RawAflDbType]) -> None:
    RawFlightLog.insert_many(data).execute()
    print("Data added to db")

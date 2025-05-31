from typing import List
from database.models import TestFlightLog
from local_types.data_type import RawAflDbType


def load_to_db(data: List[RawAflDbType]) -> None:
    TestFlightLog.insert_many(data).execute()
    print("Data added to db")

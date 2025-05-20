from typing import List
from database.models import TestFlightLog
from local_types.data_type import AflDataType


def load_to_db(data: List[AflDataType]) -> None:
    # data = df.to_dicts()
    TestFlightLog.insert_many(data).execute()
    print("Data added to db")

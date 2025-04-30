from typing import List
from sheets import async_get_afl, AFL_YEARS
import asyncio
import polars as pl
from local_types.data_type import AflDataType


def extract_afl_from_sheet(year: AFL_YEARS) -> List[AflDataType]:
    afl = asyncio.run(async_get_afl(year))
    # df = pl.from_dicts(afl)
    # return df
    return afl

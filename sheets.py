import asyncio
import time
from typing import List, Literal, TypedDict
from google.oauth2.service_account import Credentials
import gspread_asyncio
from prefect_gcp import GcpCredentials
from prefect.variables import Variable

AFL_YEARS = Literal[
    "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"
]


class AFLMetadata(TypedDict):
    id: str
    db_sheetname: str


AFL_METADATA_TYPES = dict[str, AFLMetadata]

# with open("D:/projects/data_sources/AFL/metadata.json", "r") as f:
#     AFL_URLS: dict[
#         Literal["2025", "2024", "2023", "2022", "2021", "2018", "2017", "2016"],
#         AFLMetadata,
#     ] = json.load(f)


def __get_creds__():
    gcp_credentials_block = GcpCredentials.load("analyst-gcp")
    creds = gcp_credentials_block.get_credentials_from_service_account()

    if type(creds) is not Credentials:
        raise TypeError("Credentials are not of type Credentials")

    scoped = creds.with_scopes(
        [
            "https://www.googleapis.com/auth/spreadsheets",
            # "https://www.googleapis.com/auth/drive",
        ]
    )
    return scoped


async def __async_get_worksheet__(spreadsheet_id: str, worksheet_name: str):
    try:
        agcm = gspread_asyncio.AsyncioGspreadClientManager(__get_creds__)
        agc = await agcm.authorize()
        spreadsheet = await agc.open_by_key(spreadsheet_id)
        worksheet = await spreadsheet.worksheet(worksheet_name)
        return worksheet
    except Exception as e:
        print(f"Error occurred for year: {spreadsheet_id}")
        print(f"Exception: {e}")
        raise


async def async_get_afl(
    year: AFL_YEARS,
):
    AFL_URLS = await Variable.aget("afl_metadata")  # type: ignore

    worksheet = await __async_get_worksheet__(
        AFL_URLS[year]["id"], AFL_URLS[year]["db_sheetname"]
    )
    data = await worksheet.get_all_records()
    return data


# async def fetch_all_afl():
#     afl = {}
#     tasks = {
#         year: asyncio.create_task(__async_get_afl__(year)) for year in AFL_URLS.keys()
#     }
#     results = await asyncio.gather(*tasks.values())
#     afl = dict(zip(tasks.keys(), results))
#     return afl


async def fetch_afl(year: AFL_YEARS):
    afl = await __async_get_afl__(year)
    return afl


def write_afl_to_csv(afl: dict[str, List[List[str]]]):
    for year, data in afl.items():
        with open(f"output/{year}.csv", "w") as f:
            for row in data:
                f.write(";".join(row) + "\n")


def extract_afl_from_sheet(year: AFL_YEARS):
    afl = asyncio.run(__async_get_afl__(year))
    return afl


if __name__ == "__main__":
    start_time = time.time()
    # test = asyncio.run(fetch_all_afl())
    # print(test.keys())
    # # write_afl_to_csv(test)

    afl = asyncio.run(fetch_afl("2025"))
    print(afl[0:5])
    print("Time taken:", time.time() - start_time)

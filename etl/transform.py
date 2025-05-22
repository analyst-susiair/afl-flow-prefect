from typing import List, Optional, TypedDict, Union
from local_types.data_type import AflDataType
from sheets import AFL_YEARS

# Constants
OPTIONAL_FIELDS = (
    "sic",
    "block_off",
    "take_off_utc",
    "land_utc",
    "block_on",
    "kpa",
    "timestamp",
)

CONVERT_TO_ZERO_FIELDS = (
    # ! adult,child,infant,crew,pax will be moved to optional fields once
    "adult",
    "child",
    "infant",
    "crew",
    "pax",
    "kg",
    "landings",
    "eng1_cyc",
    "eng2_cyc",
    "fuel_depart",
    "fuel_return",
    "refuelling",
)


class AflExport(TypedDict):
    year: Optional[int]
    block_off_utc: Optional[str]


def transform_sheet_data(
    data_list: List[Union[AflDataType, AflExport]], year: AFL_YEARS
) -> List[Union[AflDataType, AflExport]]:
    """
    Transform sheet data by applying various data cleaning and transformation rules.

    Args:
        data_list: List of AFL data dictionaries to transform
        year: Year of the data to process

    Returns:
        List of transformed AFL data dictionaries
    """
    transformed_data = []

    for data in data_list:
        # Skip empty flight records
        if data["fl_serial"] == "":
            continue

        transformed_item = data.copy()
        transformed_item["year"] = int(year)
        transformed_item.pop("month_filter", None)

        # Rename fields
        for old_name, new_name in {
            "from": "from_",
            "block_off": "block_off_utc",
            "block_on": "block_on_utc",
            "timestamp": "created_at",
        }.items():
            if old_name in transformed_item:
                transformed_item[new_name] = transformed_item.pop(old_name)

        # Handle optional fields
        for field in OPTIONAL_FIELDS:
            if transformed_item.get(field) == "":
                transformed_item[field] = None

        # Convert empty strings to zero
        for field in CONVERT_TO_ZERO_FIELDS:
            if transformed_item.get(field) == "":
                transformed_item[field] = 0

        transformed_data.append(transformed_item)

    return transformed_data

from typing import Dict, List
from local_types.data_type import AflDataType, RawAflDbType
from sheets import AFL_YEARS

# Constants
OPTIONAL_FIELDS: tuple[str, ...] = (
    "sic",
    "block_off_utc",
    "take_off_utc",
    "land_utc",
    "block_on_utc",
    "kpa",
    "timestamp",
    "adult",
    "child",
    "infant",
    "crew",
    "pax",
    "kg",
    "fuel_depart",
    "fuel_return",
    "refuelling",
)

CONVERT_TO_ZERO_FIELDS: tuple[str, ...] = (
    "landings",
    "eng1_cyc",
    "eng2_cyc",
)

# Field renaming mapping
FIELD_MAPPING: Dict[str, str] = {
    "from": "from_",
    "block_off": "block_off_utc",
    "block_on": "block_on_utc",
    "timestamp": "created_at",
}


def transform_sheet_data(
    data_list: List[AflDataType], year: AFL_YEARS
) -> List[RawAflDbType]:
    """
    Transform sheet data by applying various data cleaning and transformation rules.

    Args:
        data_list: List of AFL data dictionaries to transform
        year: Year of the data to process

    Returns:
        List of transformed AFL data dictionaries
    """
    transformed_data: List[RawAflDbType] = []

    for data in data_list:
        # Skip empty flight records
        if data["fl_serial"] == "":
            continue

        transformed_item: RawAflDbType = {
            "id": data["id"],
            "year": int(year),
            "fl_serial": str(data["fl_serial"])
            if len(str(data["fl_serial"])) >= 6
            else f"{data['fl_serial']:06}",
            "ac": data["ac"],
            "date": data["date"],
            "pic": data["pic"],
            "sic": data.get("sic"),
            "from_": data["from"],
            "to": data["to"],
            "dep": data["dep"],
            "arr": data["arr"],
            "customer": data["customer"],
            "block_off_utc": data.get("block_off"),
            "take_off_utc": data.get("take_off_utc"),
            "land_utc": data.get("land_utc"),
            "block_on_utc": data.get("block_on"),
            "adult": data.get("adult"),
            "child": data.get("child"),
            "infant": data.get("infant"),
            "crew": data.get("crew"),
            "pax": data.get("pax"),
            "kg": data.get("kg"),
            "start": data["start"],
            "end": data["end"],
            "hours": data["hours"],
            "landings": data["landings"],
            "eng1_cyc": data["eng1_cyc"],
            "eng2_cyc": data["eng2_cyc"],
            "fuel_depart": data["fuel_depart"],
            "fuel_return": data["fuel_return"],
            "refuelling": data.get("refuelling"),
            "base": data.get("base"),
            "area": data.get("area"),
            "kpa": data.get("kpa") or data.get("contract"),
            "ac_type": data.get("ac_type"),
            "admin": data.get("admin"),
            "created_at": data.get("timestamp"),
        }

        # Rename fields
        for old_name, new_name in FIELD_MAPPING.items():
            if old_name in transformed_item:
                transformed_item[new_name] = transformed_item.pop(old_name)

        # Handle optional fields
        for field in OPTIONAL_FIELDS:
            if field in transformed_item and transformed_item[field] == "":
                transformed_item[field] = None

        # Convert empty strings to zero
        for field in CONVERT_TO_ZERO_FIELDS:
            if field in transformed_item and transformed_item[field] == "":
                transformed_item[field] = 0

        transformed_data.append(transformed_item)

    return transformed_data

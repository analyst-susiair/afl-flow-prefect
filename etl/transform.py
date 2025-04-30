import polars as pl
from typing import List, Optional, TypedDict, Union
from local_types.data_type import AflDataType
from sheets import AFL_YEARS


class AflExport(TypedDict):
    year: Optional[int]
    block_off_utc: Optional[str]


def fill_empty_string(expr: pl.Expr, fill_value: str | None) -> pl.Expr:
    return pl.when(expr == "").then(fill_value).otherwise(expr).name.keep()


def filter_df_by_db_id(db_last_id: int, df: pl.DataFrame) -> pl.DataFrame:
    """
    Filters the DataFrame to include only rows with IDs greater than db_last_id.
    """
    return df.filter(pl.col("id") > db_last_id)


def transform_new_format(df: pl.DataFrame) -> pl.DataFrame:
    df_transformed = (
        df.filter(pl.col("fl_serial") != "")
        .with_columns(
            # pl.col("id").cast(pl.Int32),
            # pl.col("fl_serial").cast(pl.Int32),
            pl.col("sic").pipe(fill_empty_string, None),
            # pl.col("adult").str.replace("", "0").cast(pl.Int32),
            # pl.col("child")
            # .str.replace("", "0")
            # .cast(
            #     pl.Int32,
            # ),
            # pl.col("infant").str.replace("", "0").cast(pl.Int32),
            # pl.col("crew").str.replace("", "0").cast(pl.Int32),
            # pl.col("pax").str.replace("", "0").cast(pl.Int32),
            # pl.col("kg").str.replace(",", "").replace("", "0").cast(pl.Float32),
            # pl.col("start").str.replace(",", "").cast(pl.Float64).round(2),
            # pl.col("end").str.replace(",", "").cast(pl.Float64).round(2),
            pl.col("block_off").pipe(fill_empty_string, None),
            pl.col("take_off_utc").pipe(fill_empty_string, None),
            pl.col("land_utc").pipe(fill_empty_string, None),
            pl.col("block_on").pipe(fill_empty_string, None),
            # pl.col("hours").cast(pl.Float64),
            # pl.col("landings").str.replace(r"^\s*$", "0").cast(pl.Int8),
            # pl.col("eng1_cyc").str.replace(r"^\s*$", "0").cast(pl.Int8),
            pl.col("eng2_cyc").str.replace(r"^\s*$", "0").cast(pl.Int8),
            # pl.col("fuel_depart").str.replace(",", "").replace("", "0").cast(pl.Int32),
            # pl.col("fuel_return").str.replace(",", "").replace("", "0").cast(pl.Int32),
            pl.col("refuelling").str.replace(",", "").replace("", "0").cast(pl.Int32),
            pl.col("kpa").pipe(fill_empty_string, None),
            pl.col("timestamp").pipe(fill_empty_string, None),
        )
        .rename(
            {
                "from": "from_",
                "block_off": "block_off_utc",
                "block_on": "block_on_utc",
                "timestamp": "created_at",
            }
        )
    )
    return df_transformed


def transform_sheet_data(
    data_list: List[Union[AflDataType, AflExport]], year: AFL_YEARS
) -> List[Union[AflDataType, AflExport]]:
    # Function implementation here
    transformed_data = []
    for data in data_list:
        transformed_item = data.copy()  # Create a copy to avoid modifying original data
        transformed_item["year"] = int(year)
        transformed_item.pop("month_filter", None)

        # Rename fields
        if "from" in transformed_item:
            transformed_item["from_"] = transformed_item.pop("from")
        if "block_off" in transformed_item:
            transformed_item["block_off_utc"] = transformed_item.pop("block_off")
        if "block_on" in transformed_item:
            transformed_item["block_on_utc"] = transformed_item.pop("block_on")
        if "timestamp" in transformed_item:
            transformed_item["created_at"] = transformed_item.pop("timestamp")

        # Handle optional fields
        OPTIONAL_FIELDS = (
            "sic",
            "block_off",
            "take_off_utc",
            "land_utc",
            "block_on",
            "kpa",
            "timestamp",
        )
        for field in OPTIONAL_FIELDS:
            if transformed_item.get(field) == "":
                transformed_item[field] = None

        # Convert empty strings to zero
        convert_to_zero_fields = ("eng2_cyc", "fuel_return", "refuelling", "kg")
        for field in convert_to_zero_fields:
            if transformed_item.get(field) == "":
                transformed_item[field] = 0

        transformed_data.append(transformed_item)

    return transformed_data

from typing import Optional, TypedDict


class AflDataType(TypedDict):
    id: int
    fl_serial: int
    ac: str
    date: str
    pic: str
    sic: Optional[str]
    from_: str
    to: str
    dep: str
    arr: str
    customer: str
    block_off: Optional[str]
    take_off_utc: Optional[str]
    land_utc: Optional[str]
    block_on: Optional[str]
    adult: int
    child: int
    infant: int
    crew: int
    pax: int
    kg: float
    start: float
    end: float
    hours: float
    landings: int
    eng1_cyc: int
    eng2_cyc: str | int
    fuel_depart: int
    fuel_return: int
    refuelling: str | int
    base: str
    area: str
    kpa: Optional[str]
    ac_type: str
    month_filter: str
    admin: str
    timestamp: Optional[str]

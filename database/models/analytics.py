from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    FloatField,
    AutoField,
    DateTimeField,
)

from database.db import BaseModel

SCHEMA = "analytics"


class Pilot(BaseModel):
    class Meta:
        table_name = "pilot"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    name = CharField()
    position = CharField(null=True)
    status = CharField(null=True)


class Area(BaseModel):
    class Meta:
        table_name = "area"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    area = CharField(index=True)


class Base(BaseModel):
    class Meta:
        table_name = "base"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    base = CharField(index=True)


class Airport(BaseModel):
    class Meta:
        table_name = "airport"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    iata_code = CharField(index=True)
    icao_code = CharField(index=True)
    name = CharField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    area_id = ForeignKeyField(Area, null=True, backref="airports")
    base_id = ForeignKeyField(Base, null=True, backref="airports")


class Customer(BaseModel):
    class Meta:
        table_name = "customer"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    customer = CharField(index=True)


class Admin(BaseModel):
    class Meta:
        table_name = "admin"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    name = CharField(index=True)


class Kpa(BaseModel):
    class Meta:
        table_name = "kpa"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    name = CharField(index=True)
    year = IntegerField(index=True)
    base_id = ForeignKeyField(Base, null=True, backref="kpas")


class NewAflDbType(BaseModel):
    class Meta:
        table_name = "new_afl_db_type"
        schema = SCHEMA

    id = AutoField(primary_key=True)
    year = IntegerField(index=True)
    fl_serial = CharField(index=True)
    aircraft_id = IntegerField()
    date = CharField(index=True)
    pic_id = ForeignKeyField(Pilot)
    sic_id = ForeignKeyField(Pilot, null=True)
    origin_id = ForeignKeyField(Airport, backref="flights_from")
    destination_id = ForeignKeyField(Airport, backref="flights_to")
    customer_id = ForeignKeyField(Customer)
    block_off_utc = DateTimeField(null=True)
    take_off_utc = DateTimeField(null=True)
    land_utc = DateTimeField(null=True)
    block_on_utc = DateTimeField(null=True)
    adult = IntegerField(null=True)
    child = IntegerField(null=True)
    infant = IntegerField(null=True)
    crew = IntegerField(null=True)
    pax = IntegerField(null=True)
    kg = FloatField(null=True)
    start = FloatField()
    end = FloatField()
    hours = FloatField()
    landings = IntegerField()
    eng1_cyc = IntegerField()
    eng2_cyc = IntegerField(null=True)
    fuel_depart = IntegerField()
    fuel_return = IntegerField()
    refuelling = IntegerField(null=True)
    base_id = ForeignKeyField(Base, null=True)
    kpa_id = ForeignKeyField(Kpa, null=True)
    admin_id = ForeignKeyField(Admin, null=True)
    created_at = CharField(null=True)

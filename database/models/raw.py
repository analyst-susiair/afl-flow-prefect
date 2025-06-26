from peewee import CharField, IntegerField, FloatField, AutoField, DateField, TimeField

from database.db import BaseModel


class RawFlightLog(BaseModel):
    class Meta:
        # table_name = "raw_flight_log"
        table_name = "raw_flight_log"
        schema = "public"

    id = AutoField(primary_key=True)
    year = IntegerField(index=True)
    fl_serial = CharField(index=True)
    ac = CharField()
    date = DateField()
    dep = CharField()
    arr = CharField()
    pic = CharField()
    sic = CharField(null=True)
    from_ = CharField(column_name="from", null=True)  # Note the column name override
    to = CharField(null=True)
    customer = CharField()
    block_off_utc = TimeField(null=True)
    take_off_utc = TimeField(null=True)
    land_utc = TimeField(null=True)
    block_on_utc = TimeField(null=True)
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
    base = CharField(null=True)
    area = CharField(null=True)
    kpa = CharField(null=True)
    ac_type = CharField(null=True)
    admin = CharField(null=True)
    created_at = CharField()

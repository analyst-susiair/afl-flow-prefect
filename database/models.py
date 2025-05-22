from peewee import Model, CharField, IntegerField, FloatField, AutoField
from prefect.variables import Variable


class BaseModel(Model):
    @classmethod
    def bind_database(cls, db_instance):
        cls._meta.database = db_instance


class TestFlightLog(BaseModel):
    class Meta:
        table_name = "update_test_raw_flight_log"

    id = AutoField(primary_key=True)
    year = IntegerField(index=True)
    fl_serial = CharField(index=True)
    ac = CharField()
    date = CharField(index=True)
    dep = CharField()
    arr = CharField()
    pic = CharField()
    sic = CharField(null=True)
    from_ = CharField(column_name="from", null=True)  # Note the column name override
    to = CharField(null=True)
    customer = CharField()
    block_off_utc = CharField(null=True)
    take_off_utc = CharField(null=True)
    land_utc = CharField(null=True)
    block_on_utc = CharField(null=True)
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

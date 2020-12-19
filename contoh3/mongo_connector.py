from mongoengine import *
import os

connect(username="",
        password="",
        host=os.environ["MONGO_HOST"],
        port=int(os.environ["MONGO_PORT"]),
        db=os.environ["MONGO_DB"],
        authentication_source="admin")


class HotelCancellation(Document):
    lead_time = IntField(required=True)
    stays_in_week_nights = IntField(required=True)
    deposit_type = IntField(required=True)
    adr = IntField(required=True)
    total_customer = IntField(required=True)
    is_cancelled = StringField(required=True)

    meta = {
        "collection": "results",
        "allow_inheritance": True
    }


def save_to_mongo(results):
    HotelCancellation(
        lead_time=results["lead_time"],
        stays_in_week_nights=results["stays_in_week_nights"],
        deposit_type=results["deposit_type"],
        adr=results["adr"],
        total_customer=results["total_customer"],
        is_cancelled=results["is_cancelled"]
    ).save()

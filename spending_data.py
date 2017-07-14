import sys
from bson.objectid import ObjectId
from datetime import datetime, date, timedelta
from pymongo import MongoClient
import logging
from jinny_spends_cfg import *

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.Expense
consume = db.consume

def load_3D_expense():
    logging.info("Entered spending_data.load_3D_expense()")
    day_back = 2
    from_date = datetime.combine(date.today(), datetime.min.time()) - timedelta(days=day_back)

    logging.info("Returning spending_data.load_3D_expense()")
    return consume.find({"date": { "$gte" : from_date }})

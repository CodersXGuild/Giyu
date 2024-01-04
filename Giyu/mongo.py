import asyncio
import sys
from motor import motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from Giyu.confing import get_int_key, get_str_key

client = MongoClient("mongodb+srv://Giyu:SLCqD7H5mM3Q2FTG@cluster0.rmon7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
, 27017)["Giyu"]
motor = motor_asyncio.AsyncIOMotorClient("mongodb+srv://Giyu:SLCqD7H5mM3Q2FTG@cluster0.rmon7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
, 27017)
db = motor["Giyu"]
db = client["Giyu"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))

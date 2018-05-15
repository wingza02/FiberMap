from pymongo import MongoClient
import pymongo
from datetime import datetime
import json
import datetime,time
from snmp import *
from db import *
from config import ip,lat,lng

uri = "mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg"
client = MongoClient(uri)
db = client['appharbor_j9h62tbg']

def autoInc_bandwidth():
    col = db.bandwidth
    last_id = col.find().sort([
        ("_id", pymongo.DESCENDING)
    ]).limit(1)
    try:
        return last_id[0]['_id']
    except:
        return 0

def autoInc_cpu():
    col = db.cpu
    last_id = col.find().sort([
        ("_id", pymongo.DESCENDING)
    ]).limit(1)
    try:
        return last_id[0]['_id']
    except:
        return 0

def mongo_bandwidth(last_id,device_id,typeport,band_in,band_out,ifspeed):
    col = db.bandwidth
    data = {"_id":last_id,"device_id":device_id, "if_type":typeport, "inbound":band_in, "outbound":band_out, "ifspeed":ifspeed, "timestamp":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    result = col.insert_one(data)

def mongo_cpu(last_id,device_id,cpu):
    col = db.cpu
    data = {"_id":last_id,"device_id":device_id, "cpu":cpu, "timestamp":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    result = col.insert_one(data)
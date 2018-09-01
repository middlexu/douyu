# -*- encoding: utf-8 -*-

from pymongo import MongoClient
from urllib.parse import quote_plus


MONGO_TABLE = '318625'

host = '127.0.0.1'
client = MongoClient(host)
client.douyu.authenticate("douyu", "password", mechanism='SCRAM-SHA-1')
db = client["douyu"]


collection = db[MONGO_TABLE]

collection.insert({'name': 'F5'})

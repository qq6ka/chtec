# -*- coding: utf-8 -*-
import redis, pymongo
from pymongo import Connection
from bson.objectid import ObjectId

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=4)
connection = Connection('127.0.0.1', 27017, **{
	'network_timeout':30,
	'connectTimeoutMS':30000, 
	'socketTimeoutMS':30000,
	'waitQueueTimeoutMS':30000,
	'auto_start_request':False
	})
db = connection['alldevices']
db_arch = connection['archives']
reportsdb=connection['reportsdb']
items=db['items']
global_settings=db['global_settings']
average_hour=db_arch['average_hour']
average_day=db_arch['average_day']
coal=db_arch['coal']
test=db_arch['test']
sorted_c=db['sorted']
cells=reportsdb['cells']
reports=reportsdb['reports']
cells_properties=reportsdb['cells_properties']
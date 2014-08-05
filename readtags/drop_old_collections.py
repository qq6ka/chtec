# -*- coding: utf-8 -*-
from config_project import *
import time, datetime
from bson.objectid import ObjectId
from datetime import *

collections=[]
for collection in db_arch.collection_names():
	try:
		ts = datetime.now()
		delta = timedelta(days=60)
		border=ts-delta
		border=datetime(border.year,border.month,border.day,border.hour)
		if datetime.strptime(collection, '%Y-%m-%d %H:%M:%S') < border:
			# print collection
			db_arch[collection].drop()
	except Exception as err:
		pass
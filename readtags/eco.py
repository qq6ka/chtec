#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, datetime, sys, redis
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId



ts=datetime.now()
print datetime(ts.year,ts.month,ts.day)

# def get_group_id(env):
# 	return str(items.find_one({'type':'group','environment':env})['_id'])

# all_ka=['ka-7']

# for ka in all_ka:
# 	sum_dv=0
# 	sum_ds=0
# 	sum_mmt=0
# 	result_dv={}
# 	result_ds={}
# 	result_mmt={}
# 	# Выбираем нужные теги
# 	tags=items.find({"type":"tag", "$and":[{'groups':{'$in':[get_group_id(ka)]}}, {'groups':{'$in':[get_group_id('all_dutyevye'),get_group_id('all_mmt'),get_group_id('all_dymosos')]}}]})
# 	# Температура пп за котлом. Вытаскиваем из редиса. Если нет значения - не считаем ничего.
# 	try:
# 		qpp=items.find_one({'type':'tag','groups':{'$in':[get_group_id(ka)], '$in':[get_group_id('all_Q_pp_after_KA')]}})['tag_name']
# 		Qpp=float(r.hget(qpp, 'value'))
# 	except:
# 		Qpp = items.find_one({'type':'tag','groups':{'$in':[get_group_id(ka)], '$in':[get_group_id('all_Q_pp_after_KA')]}})['tag_name']

# 	if Qpp:
# 		# collections=[]
# 		# for collection in db_arch.collection_names():
# 		# 	try:
# 		# 		datetime.strptime(collection, '%Y-%m-%d %H:%M:%S')
# 		# 		collections.append(collection)
# 		# 	except:
# 		# 		pass
# 		# collections.reverse()

# 		# Получаем 20 последних значе
# 		collections=db_arch.collection_names()
# 		collections.reverse()
# 		collections=collections[0:23]
# 		for tag in tags:
# 			last_20_values=[]
# 			for collection in collections:
# 				values=db_arch[collection].find({'tag_id':tag['_id'], "value":{"$ne":"Error"}}, {'value':1, 'name':1, 'time':1, '_id':0}).limit(20).sort('_id',-1)
# 				for value in values:
# 					if len(last_20_values)<20:
# 						last_20_values.append(value)
# 					else:
# 						break
# 				if len(last_20_values)>=20:
# 					break

# 			if float(last_20_values[0]['value'])>0:
# 				dvalue = float(last_20_values[0]['value'])-float(last_20_values[-1]['value'])
# 				dtime = float(last_20_values[0]['time'])-float(last_20_values[-1]['time'])
# 			else:
# 				dvalue = 0
# 				dtime = 1

			
# 			if get_group_id('all_dutyevye') in tag['groups']:
# 				sum_dv = sum_dv+dvalue/dtime*3600
# 				result_dv[tag['name']]=dvalue/dtime*3600
# 			elif get_group_id('all_mmt') in tag['groups']:
# 				sum_mmt = sum_mmt+dvalue/dtime*3600
# 				result_mmt[tag['name']]=dvalue/dtime*3600
# 			elif get_group_id('all_dymosos') in tag['groups']:
# 				sum_ds = sum_ds+dvalue/dtime*3600
# 				result_ds[tag['name']]=dvalue/dtime*3600

			
# 			vhour = dvalue/dtime*3600
# 			hour_dv_ds = sum_dv+sum_ds
# 			day_dv_ds = hour_dv_ds*24
# 			day_sum_mmt = sum_mmt*24
# 			print "-"*20
# 			print tag['name']
# 			print vhour
# 		# print result_ds, result_mmt, result_dv
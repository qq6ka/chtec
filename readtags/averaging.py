#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, datetime, sys, redis, os
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId

def averaging(period, average_type, db_id=None):
	# TODO переписать выбор тегов по группе
	if average_type == 'mean':
		tags=items.find({'interview':True, 'type':'tag', 'groups':{'$in':['52363c5076c8151134b29e93']}})
	elif average_type == 'total':
		tags=items.find({'interview':True, 'type':'tag', 'groups':{'$in':['52363b9b76c8151134b29e91']}})
	elif average_type == 'consumption':
		tags=items.find({'interview':True, 'type':'tag', 'groups':{'$in':['52562b2f080b373dd9417d27']}})

	ts=datetime.now()
	avg_coll=ts.strftime('%Y-%m')
	avg_coll=db_arch[avg_coll]

	if period == 'hour':
		data=db_arch[db_id]
		delta = timedelta(hours=1)
		new_period=ts-delta
		start=datetime(new_period.year,new_period.month,new_period.day,new_period.hour)
		end=datetime(ts.year,ts.month,ts.day,ts.hour)
		start = time.mktime(start.timetuple())
		end = time.mktime(end.timetuple())
		for tag in tags:
			in_time=data.find({'tag_id':tag['_id'], 'value':{'$ne':'Error'}}, {'value':1, '_id':0})
			try:
				if average_type in ('mean', 'consumption'):
					result=sum(float(v['value']) for v in in_time)/in_time.count()

				elif average_type == 'total':
					result=sum(float(v['value']) for v in in_time)

				average=({'value':repr(result),'start':start,'end':end, 'type':average_type, 'tag_id':tag['_id']})
				avg_coll.insert(average)
			except Exception as e:
				predecessor=avg_coll.find({'tag_id':tag['_id'], 'type':average_type}).limit(1).sort('_id',-1)
				for p_tag in predecessor:
					average=({'value':p_tag['value'],'start':start,'end':end, 'type':average_type, 'tag_id':tag['_id']})
					avg_coll.insert(average)

	elif period=='day':
		delta = timedelta(days=1)
		new_period=ts-delta
		start=datetime(new_period.year,new_period.month,new_period.day)
		end=datetime(ts.year,ts.month,ts.day)
		start = time.mktime(start.timetuple())
		end = time.mktime(end.timetuple())
		print avg_coll, start, end
		for tag in tags:
			in_time=avg_coll.find({'tag_id':tag['_id'], 'type':average_type, 'start':{'$gte':start}, 'end':{'$lt':end}}, {'value':1, '_id':0})
			try:
				if average_type=='mean':
					result=sum(float(v['value']) for v in in_time)/in_time.count()
				elif average_type in ('total','consumption'):
					result=sum(float(v['value']) for v in in_time)

				average=({'err_state':0, 'value':repr(result),'start':start,'end':end, 'type':average_type, 'tag_id':tag['_id']})
				average_day.insert(average)
			except Exception as e:
				pass
	else:
		pass

if __name__ == "__main__":
	if sys.argv[1] == 'day':
		averaging(sys.argv[1], 'mean')
		averaging(sys.argv[1], 'total')
		averaging(sys.argv[1], 'consumption')
	elif sys.argv[1] == 'hour':
		ts=datetime.now()
		delta = timedelta(hours=1)
		db_id=datetime(ts.year,ts.month,ts.day,ts.hour)-delta
		averaging(sys.argv[1], 'mean', db_id.strftime('%Y-%m-%d %H:%M:%S'))
		averaging(sys.argv[1], 'total', db_id.strftime('%Y-%m-%d %H:%M:%S'))
		averaging(sys.argv[1], 'consumption', db_id.strftime('%Y-%m-%d %H:%M:%S'))
	else:
		pass


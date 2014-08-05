#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, datetime, sys, argparse, redis, error_collector
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId
import device as device_type
import Pyro4

e_logger=error_collector.Error_Logger()


##############################
#
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# python read_arch_tags.py тип_данных дата устройство
# python read_arch_tags.py 1_d_repeat 29.05.2014 528d65f9080b3744c93d7c85
#
# Без указания даты и устройства вычитываются все приборы за предыдущий день
# Без указания устройства вычитываются все приборы за указанный день
# С указанием даты и устройства вычитывется устройство за указанную дату
#
##############################




def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument ('group')
	parser.add_argument ('date', nargs='?')
	parser.add_argument ('device', nargs='?')

	return parser

def get_buses(group, date=None, device=None):
	e_logger("read_archives", "="*80, "START READ ARCHIVES")

	todo=Pyro4.Proxy("PYRO:todo@localhost:5150")
	gid=items.find_one({'environment':group}, {'_id':1})

	if group == '1_h_repeat':
		ts=datetime.now()
		start=datetime(ts.year,ts.month,ts.day,ts.hour)
		end=start-timedelta(hours=1)
		end=datetime(end.year,end.month,end.day,end.hour)
	else:
		if date:
			ts=time.strptime(date, "%d.%m.%Y")
			ts=datetime(ts.tm_year,ts.tm_mon,ts.tm_mday)+timedelta(days=1)
		else:
			ts=datetime.now()

		start=datetime(ts.year,ts.month,ts.day)
		end=start-timedelta(days=1)
		end=datetime(end.year,end.month,end.day)
	
	if device:
		# Указано конкретное устройство
		device = items.find_one({'type':'device', '_id':ObjectId(device)})
		bus=items.find_one({'type':'bus', '_id':ObjectId(device['parent'])})
		tags=items.find({'parent':ObjectId(device['_id']), 'interview':True, 'groups':{'$in':[str(gid['_id'])]}})
		if tags.count() > 0:
			for tag in tags:
				if group == '1_h_repeat':
					tag['arch_parameter']=tag['arch_parameter']-1
				todo.add(bus['_id'], [bus['port_address'], bus['port_baudrate'], bus['timeout'], device['dad'], device['sad'], '', tag['channel'], tag['arch_parameter'], start, end, group, str(tag['_id']), 'read_arch'])
	else:
		# Вычитываем все устройства
		buses=items.find({'type':'bus', 'interview':True})
		for bus in buses:
			devices=items.find({'type':'device', 'interview':True, 'parent':ObjectId(bus['_id'])})
			for device in devices:
				tags=items.find({'parent':ObjectId(device['_id']), 'interview':True, 'groups':{'$in':[str(gid['_id'])]}})
				if tags.count() > 0:
					for tag in tags:
						if group == '1_h_repeat':
							tag['arch_parameter']=tag['arch_parameter']-1
						todo.add(bus['_id'], [bus['port_address'], bus['port_baudrate'], bus['timeout'], device['dad'], device['sad'], '', tag['channel'], tag['arch_parameter'], start, end, group, str(tag['_id']), 'read_arch'])


if __name__ == "__main__":
	parser = createParser()
	namespace = parser.parse_args()

	get_buses(namespace.group, namespace.date, namespace.device)

# -*- coding: utf-8 -*-
import collections
import Pyro4
import datetime, time
from datetime import datetime, timedelta

sys.path.append("/home/root2/mptt/readtags")
from config_project import *

devices = items.find({'type':'device', 'modification':'logika'})
todo=Pyro4.Proxy("PYRO:todo@localhost:5150")

# Ждем, пока не будет ответа в редисе
def get_response(tmp_name):
	end = datetime.now()+timedelta(seconds=6)
	result = None
	while datetime.now()<=end:
		result = r.hgetall(tmp_name)
		if result:
			r.delete(tmp_name)
			break

	return result

for device in devices:
	bus=items.find_one({"type":"bus", "_id":ObjectId(device['parent'])})
	tags_hash={}
	date_time=""

	# Вычитываем время
	tags_hash['tagname']=[0,60]
	tmp_name=str(ObjectId())
	mrequest=[device['dad'], device['sad'], tags_hash, bus['port_address'], bus['port_baudrate'], bus['timeout'], tmp_name, 'read_value']
	todo.add(bus['_id'], mrequest, 1)
	result=get_response(tmp_name)
	if "status" in result and result['status']=="Ok":
		result = eval(result['result'])
		for value in result.values():
			date_time += value

	# Вычитываем время
	tags_hash['tagname']=[0,61]
	tmp_name=str(ObjectId())
	mrequest=[device['dad'], device['sad'], tags_hash, bus['port_address'], bus['port_baudrate'], bus['timeout'], tmp_name, 'read_value']
	todo.add(bus['_id'], mrequest, 1)
	result=get_response(tmp_name)
	if "status" in result and result['status']=="Ok":
		result = eval(result['result'])
		for value in result.values():
			date_time += "T"+value

	# Преобразуем строку в дату и сравниваем и т.д.
	try:
		date_time_obj = datetime.strptime(date_time, '%d-%m-%yT%H:%M:%S')
		timestamp_device = time.mktime(date_time_obj.timetuple())
		timestamp_now = time.time()
		timestamp_delta = timestamp_now - timestamp_device
		# Прибор отстает
		if timestamp_delta > 0:
			if timestamp_delta > 59:
				set_delta = 59
			else:
				set_delta = int(timestamp_delta)
			# print bus['name'], device['name']
			# print "Отстает на ", timestamp_delta, " устанавливаем ", set_delta
		# Прибор спешит
		else:
			if abs(timestamp_delta) > 59:
				set_delta = -59
			else:
				set_delta = int(timestamp_delta)
			# print bus['name'], device['name']
			# print "Спешит на ", abs(timestamp_delta), " устанавливаем ", set_delta
		# Пишем в прибор значение смещения времени
		tags_hash['tagname']=[0,22,set_delta]
		tmp_name=str(ObjectId())
		mrequest=[device['dad'], device['sad'], tags_hash, bus['port_address'], bus['port_baudrate'], bus['timeout'], tmp_name, 'write_value']
		todo.add(bus['_id'], mrequest, 1)
		result=get_response(tmp_name)
	except:
		pass
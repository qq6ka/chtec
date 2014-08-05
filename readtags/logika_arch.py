# -*- coding: utf-8 -*-

import serial, time, datetime, error_collector
from CRCModules.CRCCCITT import CRCCCITT
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId
import Pyro4
import sys

e_logger=error_collector.Error_Logger()

crcobj = CRCCCITT()

class Read():
	def __call__(self, request):
		# print "Запрос"
		# print request
		# [u'/dev/ttyr05', 4800, 1, 1, 6, u'1_01_1_351', 1, 406, u'2014-06-02T00:00:00', u'2014-06-01T00:00:00', u'1_d_repeat', u'528dae38080b374ccc56a4a2']
		DLE='\x10'
		SOH='\x01'
		DAD="{:c}".format(request[3])
		SAD="{:c}".format(128+request[4])
		ISI='\x1F'
		FNC='\x0E'
		STX='\x02'
		HT='\x09'
		FF='\x0C'
		ETX='\x03'

		start=time.strptime(request[-4], "%Y-%m-%dT%H:%M:%S")
		end=time.strptime(request[-3], "%Y-%m-%dT%H:%M:%S")
		arch_type=request[-2]
		tag_id=request[-1]

		# Идентификатор шины у запрашиваемого тега. Нужен для отправки в очередь.
		def get_bus_id(parent):
			device = items.find_one({'_id':ObjectId(parent)})
			bus = items.find_one({'_id':ObjectId(device['parent'])})
			return bus['_id']

		# Информация по тегу для ошибки
		tag=items.find_one({"_id":ObjectId(tag_id)})
		bus_id = get_bus_id(tag['parent'])

		mstr='{DLE}{SOH}{DAD}{SAD}{DLE}{ISI}{FNC}{DLE}{STX}{HT}{CHANNEL}{HT}{PARAMETER}{FF}{HT}{START_DAY}{HT}{START_MONTH}{HT}{START_YEAR}{HT}{START_HOUR}{HT}{START_MIN}{HT}{START_SEC}{FF}{HT}{END_DAY}{HT}{END_MONTH}{HT}{END_YEAR}{HT}{END_HOUR}{HT}{END_MIN}{HT}{END_SEC}{FF}{DLE}{ETX}'.format(
		   DLE=DLE,
		   SOH=SOH,
		   DAD=DAD,
		   SAD=SAD,
		   ISI=ISI,
		   FNC=FNC,
		   STX=STX,
		   HT=HT,
		   FF=FF,
		   ETX=ETX,
		   CHANNEL=request[6],
		   PARAMETER=request[7],
		   START_DAY=start.tm_mday,
		   START_MONTH=start.tm_mon,
		   START_YEAR=start.tm_year,
		   START_MIN=start.tm_min,
		   START_HOUR=start.tm_hour,
		   START_SEC=start.tm_sec,
		   END_DAY=end.tm_mday,
		   END_MONTH=end.tm_mon,
		   END_YEAR=end.tm_year,
		   END_HOUR=end.tm_hour,
		   END_MIN=end.tm_min,
		   END_SEC=end.tm_sec,
		)

		res = crcobj.calculate(mstr[2:])
		CRC1= "{:c}".format(res >> 8)
		CRC2= "{:c}".format(res & 0xFF)

		mstr+=CRC1+CRC2
		try:
			ser=serial.Serial(port=request[0], baudrate=request[1], timeout=request[2])
			result=self.go_read(mstr, ser, tag, arch_type, start)
			ser.close()
		except:
			result = None
		
		if result is not None:
			result = result
			err_state = 0
			e_logger("read_archives", "OK: %s" % result, tag['name'].encode("utf-8"))
		else:
			result = 0
			err_state = 1
			e_logger("read_archives", "BAD: %s" % result, tag['name'].encode("utf-8"))

			if arch_type == '1_d_repeat':
				todo=Pyro4.Proxy("PYRO:todo@localhost:5150")
				request=request+["read_arch"]
				if todo.exist_request(bus_id, request):
					todo.add(bus_id, request)
		
		ts=datetime.now()
		avg_coll=ts.strftime('%Y-%m')
		avg_coll=db_arch[avg_coll]
		if arch_type == '1_h_repeat':
			delta = timedelta(hours=1)
			start=datetime(start.tm_year,start.tm_mon,start.tm_mday,start.tm_hour)-delta
			end=start+delta
			end=datetime(end.year,end.month,end.day,end.hour)
			average=({'tag_id': ObjectId(tag_id), 'err_state':err_state, 'tagname':request[5],'value':result,'start':time.mktime(start.timetuple()),'end':time.mktime(end.timetuple())})
			avg_coll.insert(average)
		else:
			delta = timedelta(days=1)
			start=datetime(start.tm_year,start.tm_mon,start.tm_mday)-delta
			end=start+delta
			end=datetime(end.year,end.month,end.day)
			average=({'tag_id': ObjectId(tag_id), 'err_state':err_state, 'tagname':request[5],'value':result,'start':time.mktime(start.timetuple()),'end':time.mktime(end.timetuple())})
			average_day.insert(average)

	def go_read(self, request, ser, tag, arch_type, start):
		ser.flushOutput()
		ser.write(request)

		end = datetime.now()+timedelta(seconds=6)
		res=""
		while datetime.now()<=end:
			res=res+ser.readline()
			if '\x03' in res:
				time.sleep(0.3)
				res=res+ser.readline()
				break

		if len(res)>0 and repr(res[0]) == repr('\x10'):
			crc = res[-2:]
			res_crc = crcobj.calculate(res[2:-2])
			CRC1= "{:c}".format(res_crc >> 8)
			CRC2= "{:c}".format(res_crc & 0xFF)
			if crc == CRC1+CRC2:
				if arch_type == '1_h_repeat':
					try:
						return float(res.split("\x0c")[3].split("\t")[1])
					except Exception as e:
						e_logger("logika_arch", e, ["TAG:",tag,"Connection:",ser, "Request:",request, "Response:",res])
						return None
				else:
					# Суточные результаты. Приборы возвращают по разному.
					# Берем ответ, дата которого равна стартовой.
					date = res.split("\x0c")[3].split("\t")[-1].split("/")[0].strip()
					try:
						if time.strptime(date, "%d-%m-%y") == start:
							return float(res.split("\x0c")[3].split("\t")[1])
					except Exception as e:
						e_logger("logika_arch", e, ["TAG:",tag,"Connection:",ser, "Request:",request, "Response:",res])
						return None

					date = res.split("\x0c")[4].split("\t")[-1].split("/")[0].strip()
					try:
						if time.strptime(date, "%d-%m-%y") == start:
							return float(res.split("\x0c")[4].split("\t")[1])
					except Exception as e:
						e_logger("logika_arch", e, ["TAG:",tag,"Connection:",ser, "Request:",request, "Response:",res])
						return None
			else:
				return None		
					
		else:
			e_logger("logika_arch", "Hand Exception", ["TAG:",tag,"Connection:",ser, "Request:",request, "Response:",res])
			return None

reader=Read()
request=eval(sys.argv[-1])
reader(request)
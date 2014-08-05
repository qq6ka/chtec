# -*- coding: utf-8 -*-
import struct, serial, time, datetime, error_collector
from datetime import datetime, timedelta

e_logger=error_collector.Error_Logger()

class Mark():
	result, status = None, None
	def __call__(self, request, ser):
		# request=[сетевой адрес, номер канала, номер функции, 0, 0] для 902
		# request=[сетевой адрес, номер канала, номер функции, 0, 0, 0, 0] для 602

		if len(request) == 5:
			self.Read902(request, ser)
		else:
			self.Read602(request, ser)

		return {'channel':request[1], 'parameter':request[2], 'status':self.status, 'result':self.result}

	def Read902(self, request, ser):
		r = struct.pack("!5b", request[0], request[1], request[2], request[3], request[4])
		crc = struct.pack("!1b", ~request[0]+~request[1]+~request[2]+~request[3]+~request[4]+1)
		mstr = chr(255) + r + crc

		ser.flushOutput()
		ser.flushInput()
		ser.write(mstr)
		res = ""
		end = datetime.now()+timedelta(seconds=6)
		while datetime.now()<=end:
			res=res+ser.read(1)
			if len(res) == 7:
				break

		if len(res) == 7:
			barray = struct.unpack("!5b", res[1:6])
			calc_crc = sum([~b for b in barray]) + 1
			crc = res[6]
			if calc_crc & 255 == ord(crc):
				first_byte = res[4]
				second_byte = res[5]
				val1 = (((ord(first_byte) & 0xF0) >> 4) * 1000 +(ord(first_byte) & 0x0F) * 100 +((ord(second_byte) & 0xF0) >> 4) * 10 +(ord(second_byte) & 0x0F))
				if ord(first_byte) >>7:
					val1 = val1 - 8000
					val1 = val1 * (-1)
				self.status = "Ok"
				self.result = val1/100.0
			else:
				self.status=u'Не совпала контрольная сумма'
				self.result='Error'
		else:
			self.status=u'Нет соединения с устройством'
			self.result='Error'

	def Read602(self, request, ser):
		r = struct.pack("!7b", request[0], request[1], request[2], request[3], request[4], request[5], request[6])
		crc = struct.pack("!1b", ~request[0]+~request[1]+~request[2]+~request[3]+~request[4]+~request[5]+~request[6]+1)
		mstr = chr(255) + r + crc

		ser.flushOutput()
		ser.flushInput()
		ser.write(mstr)
		res = ""
		end = datetime.now()+timedelta(seconds=6)
		while datetime.now()<=end:
			res=res+ser.read(1)
			if len(res) == 9:
				break

		if len(res) == 9:
			mhex = ""
			for i in res:
				mhex += " " + hex(ord(i))

			barray = struct.unpack("!7b", res[1:8])
			crc = res[8]
			calc_crc = sum([~ b for b in barray]) + 1
			if calc_crc & 255 == ord(crc):
				value = struct.unpack("f", res[4:8])
				self.status = "Ok"
				self.result = value[0]
			else:
				self.status=u'Не совпала контрольная сумма'
				self.result='Error'
		else:
			self.status=u'Нет соединения с устройством'
			self.result='Error'
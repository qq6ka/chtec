# -*- coding: utf-8 -*-

import serial, time, datetime, error_collector, sys
from CRCModules.CRCCCITT import CRCCCITT
from datetime import datetime, timedelta
from config_project import *

e_logger=error_collector.Error_Logger()

crcobj = CRCCCITT()

class Logika():
	result, status = None, None

	def __call__(self, request):
		DLE='\x10'
		SOH='\x01'
		DAD="{:c}".format(request[0])
		SAD="{:c}".format(128+request[1])
		ISI='\x1F'
		FNC='\x03'
		STX='\x02'
		HT='\x09'
		FF='\x0C'
		ETX='\x03'

		REQUEST=''
		for tag_name, tag in request[2].items():
			REQUEST = REQUEST + '{HT}%s{HT}%s{FF}{HT}%s{FF}' % (tag[0], tag[1], tag[2])
		REQUEST = REQUEST.format(HT=HT, FF=FF)

		mstr='{DLE}{SOH}{DAD}{SAD}{DLE}{ISI}{FNC}{DLE}{STX}{REQUEST}{DLE}{ETX}'.format(
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
		   REQUEST=REQUEST,
		)

		res = crcobj.calculate(mstr[2:])
		CRC1= "{:c}".format(res >> 8)
		CRC2= "{:c}".format(res & 0xFF)

		mstr+=CRC1+CRC2

		try:
			ser=serial.Serial(port=request[3], baudrate=request[4], timeout=request[5])
			self.go_read(mstr,ser)
			ser.close()
		except:
			pass

		r.hmset(request[-1], {'status':self.status, 'result':self.result})

	def go_read(self, request, ser):
		ser.flushOutput()
		ser.write(request)
		end = datetime.now()+timedelta(seconds=6)
		res=""
		while datetime.now()<=end:
			res=res+ser.readline()
			if '\x03' in res:
				break

		if len(res)>0 and repr(res[0]) == repr('\x10'):
			result={}
			try:
				tags = res.split('\x1f')[1]
				tags = tags.split('\x0C')
				tag_generator=(tag for tag in tags[:-1])
				for i in range((len(tags)-1)/2):
					channel=tag_generator.next().split('\t')
					value=tag_generator.next().split('\t')
					result[channel[1],channel[2]]=value[1]
			except Exception as e:
				e_logger("logika", e, ["Connection:",ser, "Request:",repr(request), "Response:",repr(res)])

			crc = res[-2:]
			res = crcobj.calculate(res[2:-2])
			CRC1= "{:c}".format(res >> 8)
			CRC2= "{:c}".format(res & 0xFF)

			if crc == CRC1+CRC2:
				self.status='Ok'
				self.result=result
			else:
				self.status='Bad CRC'
				self.result='Error'
		else:
			self.status=u'Not connect'
			self.result='Error'

reader=Logika()
request=eval(sys.argv[1])
reader(request)
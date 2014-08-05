# -*- coding: utf-8 -*-

import serial, time, error_collector
from math import *
from config_project import *
e_logger=error_collector.Error_Logger()

# Чтение УСО с дискретными параметрами
class Dcon7053():
	result, status = None, None

	def __call__(self, request, ser):
		ser.write(request)
		time.sleep(0.3)
		if ser.inWaiting()>0:
			try:
				result={}
				data=ser.read(ser.inWaiting())
				data=data[1:]
				data = int(data[:4],16)
				for channel in range(16):
					if int(bin(data)[-(channel+1)]) == 1:
						value=0
					else:
						value=1
					result[channel] = int(value)

				self.status='Ok'
				self.result=result
			except Exception as err:
				e_logger("dcon7053", err, "Read error from device")
				self.status=u'Ошибка чтения с устройства'
				self.result='Error'
		else:
			e_logger("dcon7053", 'No connection with device', ser.inWaiting())
			self.status=u'Нет соединения с устройством'
			self.result='Error'

		return {'status':self.status, 'result':self.result}


# Чтение УСО с аналоговыми входами
class Dcon7017():
	result, status = None, None

	def __call__(self, request, ser):
		ser.write(request)
		time.sleep(0.3)
		if ser.inWaiting()>0:
			try:
				result={}
				data=ser.read(ser.inWaiting())
				data=data[1:]
				for channel in range(8):
					ch=channel*7
					result[channel] = float(data[ch:ch+7])

				self.status='Ok'
				self.result=result
			except Exception as err:
				e_logger("dcon7017", err, "Read error from device")
				self.status=u'Ошибка чтения с устройства'
				self.result='Error'
		else:
			e_logger("dcon7017", 'No connection with device')
			self.status=u'Нет соединения с устройством'
			self.result='Error'

		return {'status':self.status, 'result':self.result}


# Вычисляем значение
class Calculate_values():
	def __call__(self, uso_name):

		def temp_value(tagname):
			return abs(float(r.hgetall(tagname)['value']))

		def write_data(tagname, value):
			from test_read_tags import Write_data
			tag=items.find_one({'type':'tag', 'short_name':tagname})
			send={}
			send['result']=float(value)
			send['status']='Ok'
			Write_data(tag, send=send)

		p   = 0.0
		tau = 0.0
		Z   = 0.0
		ro  = 0.0

		if uso_name == "USO-1":
			p  = (temp_value('КА-4 P пп за котлом USO') * 160.0 * 0.0980665 + 0.0933254)/22.064
			tau = (temp_value('КА-4 Т пп USO') * 600 + 273.15) / 647.14
			Z   = 1 + p*(0.4409392*pow(tau, -1) - 1.386598*pow(tau, -2) + 1.380501*pow(tau, -3) - 0.7644377*pow(tau, -4)) + pow(p, 2)*(56.40548*pow(tau, -1) - 297.0161*pow(tau, -2) + 617.8258*pow(tau, -3) - 634.747*pow(tau,  -4) + 322.8009*pow(tau, -5) - 65.45004*pow(tau, -6)) + pow(p, 3) *(149.3651*pow(tau, -1) - 895.0375*pow(tau, -2) + 2123.035*pow(tau, -3) - 2488.625*pow(tau, -4) + 1439.213*pow(tau, -5) - 327.7709*pow(tau, -6)) + pow(p, 4)*(151.1386 - 967.3387*pow(tau, -1) + 2478.739*pow(tau, -2) - 3178.106*pow(tau, -3) + 2038.512*pow(tau, -4) - 523.2041*pow(tau,  -5))
			if (tau *Z)!=0 :
				ro  = p*73.864969/(tau *Z)
			if temp_value('КА-4 Q пп USO') >= 0  and ro >= 0:
				write_data('КА-4 Q пп USO', sqrt(temp_value('КА-4 Q пп USO') * 1.6 * 2 * 98066.5*ro)*3.6 * 0.02306571)
			if temp_value('КА-4 Q пв перед котлом USO') >= 0  and ro >= 0:
				write_data('КА-4 Q пв перед котлом USO', sqrt(temp_value('КА-4 Q пв перед котлом USO') * 2 * 0.63 * 98066.5*854.0)*3.6*0.00684255)
			write_data('КА-4 P пп за котлом USO',temp_value('КА-4 P пп за котлом USO')*160)
			write_data('КА-4 Т пп USO',temp_value('КА-4 Т пп USO')*600)

			p = (temp_value('КА-5 P пп за котлом USO') * 160.0 * 0.0980665 + 0.0933254)/22.064
			tau = (0.89 * 600 + 273.15)/ 647.14
			Z = abs(1 + p*(0.4409392*pow(tau, -1) - 1.386598*pow(tau, -2) + 1.380501*pow(tau, -3) - 0.7644377*pow(tau, -4)) + pow(p, 2)*(56.40548*pow(tau, -1) - 297.0161*pow(tau, -2) + 617.8258*pow(tau, -3) - 634.747*pow(tau,  -4) + 322.8009*pow(tau, -5) - 65.45004*pow(tau, -6)) + pow(p, 3) *(149.3651*pow(tau, -1) - 895.0375*pow(tau, -2) + 2123.035*pow(tau, -3) - 2488.625*pow(tau, -4) + 1439.213*pow(tau, -5) - 327.7709*pow(tau, -6)) + pow(p, 4)*(151.1386 - 967.3387*pow(tau, -1) + 2478.739*pow(tau, -2) - 3178.106*pow(tau, -3) + 2038.512*pow(tau, -4) - 523.2041*pow(tau,  -5)))
			if (tau *Z)!=0 :
				ro = p*73.864969/(tau *Z)
			if temp_value("КА-5 Q пп USO") >= 0 and ro >= 0 :
				write_data("КА-5 Q пп USO", sqrt(temp_value("КА-5 Q пп USO") * 1.6 * 2 * 98066.5*ro)*3.6*0.02307199)
			if temp_value("КА-5 Q пв перед котлом USO") >= 0 and ro >= 0 :
				write_data("КА-5 Q пв перед котлом USO", sqrt(temp_value("КА-5 Q пв перед котлом USO") * 1.0197 * 2 * 98066.5*854.0)*3.6*0.00723)
			write_data("КА-5 P пп за котлом USO", temp_value("КА-5 P пп за котлом USO") * 160)
			write_data("КА-5 Т пп USO", temp_value("КА-5 Т пп USO") * 600)

		if uso_name == "USO-2":
			p = (temp_value('КА-6 P пп за котлом USO') * 160.0 * 0.0980665 + 0.0933254)/22.064
			tau = (0.89 * 600 + 273.15)/ 647.14
			Z = 1 + p*(0.4409392*pow(tau, -1) - 1.386598*pow(tau, -2) + 1.380501*pow(tau, -3) - 0.7644377*pow(tau, -4)) + pow(p, 2)*(56.40548*pow(tau, -1) - 297.0161*pow(tau, -2) + 617.8258*pow(tau, -3) - 634.747*pow(tau,  -4) + 322.8009*pow(tau, -5) - 65.45004*pow(tau, -6)) + pow(p, 3) *(149.3651*pow(tau, -1) - 895.0375*pow(tau, -2) + 2123.035*pow(tau, -3) - 2488.625*pow(tau, -4) + 1439.213*pow(tau, -5) - 327.7709*pow(tau, -6)) + pow(p, 4)*(151.1386 - 967.3387*pow(tau, -1) + 2478.739*pow(tau, -2) - 3178.106*pow(tau, -3) + 2038.512*pow(tau, -4) - 523.2041*pow(tau,  -5))
			if (tau *Z)!=0 :
				ro = p*73.864969/(tau *Z)
			if temp_value("КА-6 Q пп за котлом USO") >= 0  and ro >= 0:
				write_data("КА-6 Q пп за котлом USO", sqrt(temp_value("КА-6 Q пп за котлом USO") * 1.6 * 2 * 98066.5 * abs(ro)) * 3.6 * 0.023072)
			write_data("КА-6 Q пв перед котлом USO", sqrt(abs(temp_value("КА-6 Q пв перед котлом USO")) * 0.63 * 2 * 98066.5*854.0)*3.6*0.006865195)
			write_data('КА-6 P пп за котлом USO',temp_value('КА-6 P пп за котлом USO')*160)
			write_data('КА-6 Т пп за котлом USO',temp_value('КА-6 Т пп за котлом USO')*600)

			p = (temp_value('КА-7 P пп за котлом USO') * 160.0 * 0.0980665 + 0.0933254)/22.064
			tau = (temp_value('КА-7 Т пп за котлом USO') * 600 + 273.15) / 647.14
			Z = 1 + p*(0.4409392*pow(tau, -1) - 1.386598*pow(tau, -2) + 1.380501*pow(tau, -3) - 0.7644377*pow(tau, -4)) + pow(p, 2)*(56.40548*pow(tau, -1) - 297.0161*pow(tau, -2) + 617.8258*pow(tau, -3) - 634.747*pow(tau,  -4) + 322.8009*pow(tau, -5) - 65.45004*pow(tau, -6)) + pow(p, 3) *(149.3651*pow(tau, -1) - 895.0375*pow(tau, -2) + 2123.035*pow(tau, -3) - 2488.625*pow(tau, -4) + 1439.213*pow(tau, -5) - 327.7709*pow(tau, -6)) + pow(p, 4)*(151.1386 - 967.3387*pow(tau, -1) + 2478.739*pow(tau, -2) - 3178.106*pow(tau, -3) + 2038.512*pow(tau, -4) - 523.2041*pow(tau,  -5))
			if (tau *Z)!=0 :
				ro = p*73.864969/(tau *Z)
			if temp_value("КА-7 Q пп за котлом USO") >= 0  and ro >= 0:
				write_data("КА-7 Q пп за котлом USO", sqrt(temp_value("КА-7 Q пп за котлом USO") * 1.6 * 2 * 98066.5 * ro) *3.6 * 0.023072)
			if temp_value("КА-7 Q пв перед котлом USO") >= 0  and ro >= 0:
				write_data("КА-7 Q пв перед котлом USO", sqrt(temp_value("КА-7 Q пв перед котлом USO") * 0.63 * 2 * 98066.5*854.0)*3.6*0.00683641)
			write_data("КА-7 P пп за котлом USO", temp_value("КА-7 P пп за котлом USO")*160)
			write_data('КА-7 Т пп за котлом USO', temp_value('КА-7 Т пп за котлом USO')*600)

		if uso_name == "USO-3":
			write_data('Р АСК USO', temp_value('Р АСК USO'))

		if uso_name == "USO-4":
			write_data('ТГ-4 Т выхлоп ЦНД USO', temp_value('ТГ-4 Т выхлоп ЦНД USO') * 300)
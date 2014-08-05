# -*- coding: utf-8 -*-
import datetime, re, math
from datetime import datetime,timedelta

class Aist():
	result, status = None, None

	def __call__(self, request, ser):
		result={}
		try:
			for value in ser.read().split(";"):
				for tag in request:
					if value.split("@")[0] == str(tag):
						result[tag]=float(value.split("@")[4])
			self.result=result
			self.status='Ok'
		except Exception as e:
			self.result=result
			self.status=u'Истек период ожидания'
		finally:
			return {'status':self.status, 'result':self.result}
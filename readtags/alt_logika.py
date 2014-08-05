# -*- coding: utf-8 -*-
import datetime, re, math 
import elementtree.ElementTree as ET
from datetime import datetime,timedelta

class AltLogika():
	result, status = None, None

	def __call__(self, request, ser):
		result={}
		try:
			root = ET.fromstring(ser.read())
			for record in root.getiterator('record'):
				for tag in record.getiterator('tag'):
					result[tag.attrib['id']]=float(tag.attrib['value'])
			self.result=result
			self.status='Ok'
		except Exception as e:
			self.result=result
			self.status=u'Истек период ожидания'
		finally:
			return {'status':self.status, 'result':self.result}
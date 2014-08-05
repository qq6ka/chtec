# -*- coding: utf-8 -*-
import re, error_collector
from config_project import *
from math import *
e_logger=error_collector.Error_Logger()


class Eval_tag():
	result, status = None, None

	def __call__(self, expression):

		def tag_value(shortname):
			shortname=shortname[2:-1]
			tag=items.find_one({"short_name":shortname})
			try:
				result=r.hgetall(str(tag['_id']))['value']
				return float(result)
			except:
				return 0.0

		tags=re.findall(r'{[^}]+}', expression)
		for tag in tags:
			# print tag, tag_value(tag)
			expression=expression.replace(tag, str(tag_value(tag))).replace(u'ЕСЛИ', 'if').replace(u'ИНАЧЕ', 'else')

		try:
			result = eval(expression)
			self.status='Ok'
			self.result=result
		except Exception as err:
			e_logger("comput_tag", err, 'Error while computation')
			self.status=u'Ошибка в расчете'
			self.result='Error'

		return {'status':self.status, 'result':self.result}

# test=Eval_tag()
# print test(u"{@БУ-1 Q подающ. трубопр.}+{@БУ-2 Q подающ.}-{@КСК ГЩУ Q подающ. трубопр.}-({@БУ-1 Q прям. на отопл.} ЕСЛИ {@БУ-1 Q подающ. трубопр.}<200 ИНАЧЕ 0)")
__author__ = 'bukhval'

import serial, expression, dcon, modbus, aist, logika, alt_logika, mark, urllib2, datetime, time, error_collector, computational
from datetime import datetime

e_logger=error_collector.Error_Logger()

class Bus():
	def connect(self, connection, modification):
		if modification == 'modbus':
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)
		elif modification == 'aist-tornado':
			try:
				return urllib2.urlopen(url=connection[0], timeout=connection[1])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)
		elif modification == "mark-902":
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)
		elif modification == "mark-602":
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)
		elif modification == "logika":
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)
		elif modification=="dcon7053":
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)		
		elif modification=="dcon7017":
			try:
				return serial.Serial(port=connection[0], baudrate=connection[1], timeout=connection[2])
			except Exception as e:
				e_logger(modification, e)
				time.sleep(1)		

class Device(Bus):
	def __init__(self):
		self.type='device'

	def read_data(self, modification, connection, reader, request, bus):
		ser = bus.connect(modification=modification, connection=connection)
		if ser:
			result = reader(request,ser)
			ser.close()
			return result
		else:
			return {'status':u'Нет соединения с шиной'}

	def read_computational(self, reader, request):
		result = reader(request)
		return result

	def read_expression(self, reader, request):
		result = reader(request)
		return result

class Dcon7053(Device):
	def __init__(self, name, parent, bus, interview, connection, _id, group, device, bus_address):
		Device.__init__(self)
		self.modification='dcon7053'
		self.name=name
		self.parent=parent
		self.bus=bus
		self.interview=interview
		self.connection=connection
		self._id=_id
		self.group=group
		self.device=device
		self.bus_address=bus_address

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=dcon.Dcon7053(), request="$%02X6\r" % self.bus_address, bus=self.bus)

class Dcon7017(Device):
	def __init__(self, name, parent, bus, interview, connection, _id, group, device, bus_address):
		Device.__init__(self)
		self.modification='dcon7017'
		self.name=name
		self.parent=parent
		self.bus=bus
		self.interview=interview
		self.connection=connection
		self._id=_id
		self.group=group
		self.device=device
		self.bus_address=bus_address

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=dcon.Dcon7017(), request="#%02X\r" % self.bus_address, bus=self.bus)

class Computational(Device):
	def __init__(self, name, parent, device, bus, interview, _id, tags, group, groups):
		Device.__init__(self)
		self.modification='computational'
		self.bus=bus
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.group=group
		self.tags=tags
		self.device=device
		self.groups=groups

	def read(self):
		return self.device.read_computational(reader=computational.Computational(), request=[self.groups])


class Expression(Device):
	def __init__(self, name, parent, device, bus, interview, _id, tag, group):
		Device.__init__(self)
		self.modification='expression'
		self.bus=bus
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.group=group
		self.tag=tag
		self.device=device

	def read(self):
		return self.device.read_expression(reader=expression.Eval_tag(), request=self.tag['expression'])

class Mark902(Device):
	def __init__(self, name, parent, bus, interview, connection, _id, device, bus_address, channel, parameter, group):
		Device.__init__(self)
		self.modification='mark-902'
		self.name=name
		self.parent=parent
		self.bus=bus
		self.interview=interview
		self.connection=connection
		self._id=_id
		self.device=device
		self.bus_address=bus_address
		self.channel=channel
		self.parameter=parameter
		self.group=group

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=mark.Mark(), request=[self.bus_address, self.channel, self.parameter, 0, 0], bus=self.bus)

class Mark602(Device):
	def __init__(self, name, parent, bus, interview, connection, _id, device, bus_address, channel, parameter, group):
		Device.__init__(self)
		self.modification='mark-602'
		self.name=name
		self.parent=parent
		self.bus=bus
		self.interview=interview
		self.connection=connection
		self._id=_id
		self.device=device
		self.bus_address=bus_address
		self.channel=channel
		self.parameter=parameter
		self.group=group

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=mark.Mark(), request=[self.bus_address, self.channel, self.parameter, 0, 0, 0, 0], bus=self.bus)

class Logika(Device):
	def __init__(self, name, parent, device, connection, bus, interview, _id, tags, group, dad, sad):
		Device.__init__(self)
		self.modification='logika'
		self.bus=bus
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.connection=connection
		self.group=group
		self.tags=tags
		self.device=device
		self.dad=dad
		self.sad=sad

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=logika.Logika(), request=[self.dad,self.sad,self.tags], bus=self.bus)

class Modbus(Device):
	def __init__(self, channels, device, name, parent, interview, _id, bus_address, connection, bus, function=None, group=None):
		Device.__init__(self)
		self.modification='modbus'
		self.bus=bus
		self.channels=channels
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.bus_address=bus_address
		self.connection=connection
		self.function=function
		self.group=group
		self.device=device

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=modbus.Modbus(), request=self.function, bus=self.bus)

class Tornado(Device):
	def __init__(self, name, parent, device, connection, bus, interview, _id, tags, group):
		Device.__init__(self)
		self.modification='aist-tornado'
		self.bus=bus
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.connection=connection
		self.group=group
		self.tags=tags
		self.device=device

	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=aist.Aist(), request=self.tags, bus=self.bus)

class AltLogika(Device):
	def __init__(self, name, parent, device, bus, interview, _id, tags, group):
		Device.__init__(self)
		self.modification='alt-logika'
		self.bus=bus
		self.name=name
		self.parent=parent
		self.interview=interview
		self._id=_id
		self.group=group
		self.tags=tags
		self.device=device
		self.connection=['http://172.27.81.199:8080/OSS/bridge/queryData?queryString=select+[@value,@lastUpdate]+from+Objects[@id+in(%s)]&useScheme=graphMirror' % ",".join("'"+str(x)+"'" for x in self.tags), 5]
		
	def read(self):
		return self.device.read_data(modification=self.modification, connection=self.connection, reader=alt_logika.AltLogika(), request=self.tags, bus=self.bus)



# http://172.27.81.199:8080/OSS/bridge/queryData?queryString=select+[@value,@lastUpdate]+from+Objects[@id+in('171207')]&useScheme=graphMirror
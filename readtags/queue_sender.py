# -*- coding: utf-8 -*-

class Queue():
	def __init__(self, id):
		self.queue=[]
		self.id=id

	def add(self, request, level=None):
		if level:
			self.queue.insert(level-1,request)
		else:
			self.queue.append(request)
		
		return self.queue

	def exist(self):
		if self.queue:
			return True
		else:
			return False

	def get(self):
		return self.queue.pop(0)

	def flush(self):
		self.queue=[]

	# def __str__(self):
	# 	return '[Queue is: %s]' % self.queue
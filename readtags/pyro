import Pyro4

class ToDo(object):
	def __init__(self):
		self.qhash={}

	def add(self, bid, device, level=None):
		if bid in self.qhash:
			if level:
				self.qhash[bid]=[device]+self.qhash[bid]
			else:
				self.qhash[bid]=self.qhash[bid]+[device]
		else:
			self.qhash[bid]=[device]
		
	def exist(self, bid):
		if bid in self.qhash and len(self.qhash.get(bid))>0:
			return True
		else:
			return False

	def exist_request(self, bid, request):
		if bid in self.qhash and request not in(self.qhash.get(bid)):
			return True
		else:
			return False

	def len(self, bid):
		if bid in self.qhash and len(self.qhash.get(bid))>0:
			return len(self.qhash.get(bid))

	def get(self, bid):
		return self.qhash.get(bid).pop(0)


todo=ToDo()
daemon=Pyro4.Daemon(host="localhost", port=5150)
Pyro4.Daemon.serveSimple(
	{todo: "todo"},
	ns=False,
	daemon=daemon,
	verbose = True
)
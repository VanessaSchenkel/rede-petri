class Event(object):
	def __init__(self, name):
		self.name = name
		self.eventId = ""

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def executeEvent(self, descriptors, model):
		pass

	def recordStatistics(self, model):
		pass
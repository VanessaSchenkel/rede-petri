#from MappingStructs import FutureEventTime
#import datetime
from ModelAttributes import Descriptors, ModelAttributes
from Statistical import Statistical

class Scheduler(object):
	def __init__(self):
		self.descriptors = Descriptors()
		self.model = ModelAttributes()


	def simulate(self):
		while self.model.isFinished() == False:
			self.simulateOneStep()
		self.model.showStatistics()
		print("Terminou")


	def simulateOneStep(self):
		scheduledEvent = self.model.getNextEvent()
		# print(str(scheduledEvent.event.name) + ':' + str(scheduledEvent.scheduledTime))
		if scheduledEvent.args is None:
			scheduledEvent.event.executeEvent(self.descriptors, self.model)
			scheduledEvent.event.recordStatistics(self.model)
		else:
			scheduledEvent.event.executeEvent(self.descriptors, self.model, **scheduledEvent.args)
			scheduledEvent.event.recordStatistics(self.model)

	def simulateBy(self, duration):
		pass

	def simulateUntil(self):
		pass

	def createResource(self, resourceType, name, quantity):
		self.model.createResource(resourceType, name, quantity, self.descriptors.resources)

	def getResource(self, id):
		pass

	def scheduleNow(self, eventName, args):
		self.model.scheduleNow(eventName, self.descriptors.events, args)

	def scheduleIn(self, eventName, timeToEvent):
		self.model.scheduleIn(eventName, timeToEvent, self.descriptors.events, {})

	def scheduleAt(self, eventName, absoluteTime):
		self.model.scheduleAt(eventName, absoluteTime, self.descriptors.events, {})

	def defineEventSpecialization(self, name, event):
		self.descriptors.defineEventSpecialization(name, event)

	def defineEntitySpecialization(self, name, entity):
		self.descriptors.defineEntitySpecialization(name, entity)

	def defineResourceSpecialization(self, name, resource):
		self.descriptors.defineResourceSpecialization(name, resource)

	def defineEntitySetSpecialization(self, name, entitySet):
		self.descriptors.defineEntitySetSpecialization(name, entitySet)

	def initializeQueue(self, queueName):
		self.model.initializeQueue(queueName)

	def getEvent(self, id):
		pass

	def createEntitySet(self, name, mode, maxPossibleSize):
		pass

	def getEntitySet(self, id):
		pass





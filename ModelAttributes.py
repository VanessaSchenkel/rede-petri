import operator
from ScheduledEvent import ScheduledEvent
from EntitySet import EntitySet
from Statistical import Statistical

class Descriptors(object):
	def __init__(self):
		self.events = {}
		self.entities = {}
		self.resources = {}
		self.entitySets = {}

	def defineEventSpecialization(self, name, event):
		if name in self.events.keys():
			raise Exception('O evento ' + name + '  já foi definido.')
		else:
			self.events[name] = event

	def defineEntitySpecialization(self, name, entity):
		if name in self.entities.keys():
			raise Exception('A entidade ' + name + '  já foi definida.')
		else:
			self.entities[name] = entity

	def defineResourceSpecialization(self, name, resource):
		if name in self.resources.keys():
			raise Exception('O recurso ' + name + '  já foi definido.')
		else:
			self.resources[name] = resource

	def defineEntitySetSpecialization(self, name, entitySet):
		if name in self.entitySets.keys():
			raise Exception('A entitySets ' + name + '  já foi definida.')
		else:
			self.entitySets[name] = entitySet


class ModelAttributes(object):
	def __init__(self):
		self.FEL = []
		self.resources = {}
		self.queues = {}

		self.statistical = Statistical()

		self.start_time = 0
		self.time =  0

	def isFinished(self):
		if len(self.FEL) > 0:
			return False
		else: 
			return True

	def getTime(self):
		return self.time

	def getNextEvent(self):
		if len(self.FEL) > 0:
			self.statistical.appendStatisticalData(self.time, self.resources, self.queues)

			nextEvent = self.FEL.pop(0)
			self.time = nextEvent.scheduledTime
			print("Tempo do evento: " + str(self.time))
			print("Nome do evento: " + str(nextEvent.event.name))
			return nextEvent
		else:
			return None

	def isQueueEmpty(self, queueName):
		if self.queues[queueName].getSize() > 0:
			return False
		else:
			return True

	def removeFromQueueById(self, queueName, entityId):
		self.queues[queueName].removeEntityById(entityId)

	def insertInQueue(self, queueName, entity):
		self.queues[queueName].insert(entity)

	def popFromQueue(self, queueName):
		return self.queues[queueName].pop()

	def initializeQueue(self, queueName):
		self.queues[queueName] = EntitySet(queueName)

	def getQueueSize(self, queueName):
		return self.queues[queueName].getSize()

	def createResource(self, resourceType, name, quantity, resourceDescriptors):
		self.resources[name] = resourceDescriptors[resourceType](name, quantity)

	def createEntity(self, name, entityDescriptors, args):
		if args is not None:
			return entityDescriptors[name](name, **args)
		else:
			return entityDescriptors[name](name) 

	def isEntityInQueueById(self, queueName, id):
		return self.queues[queueName].isEntityInQueueById(id)

	def scheduleNow(self, eventName, eventDescriptors, args):
		event = eventDescriptors[eventName](eventName)
		schedule = ScheduledEvent(self.getTime(), event, args)
		self.FEL.append(schedule)
		self.FEL.sort(key=lambda x: x.getScheduledTime(), reverse=False)

	def scheduleIn(self, eventName, timeToEvent, eventDescriptors, args):
		event = eventDescriptors[eventName](eventName)
		schedule = ScheduledEvent(self.getTime()+timeToEvent, event, args)
		self.FEL.append(schedule)
		self.FEL.sort(key=lambda x: x.getScheduledTime(), reverse=False)

	def scheduleAt(self, event, absoluteTime, eventDescriptors, args):
		event = eventDescriptors[eventName](eventName)
		schedule = ScheduledEvent(absoluteTime, event, args)
		self.FEL.append(schedule)
		self.FEL.sort(key=lambda x: x.getScheduledTime(), reverse=False)

	def showStatistics(self):
		self.statistical.displayStatistics()



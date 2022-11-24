import datetime
import uuid

class Entity(object):
	def __init__(self, name,  petriNet):
		self.__init__(self, name)
		self.setPetriNet(petriNet)

	def __init__(self, name):
		self.name = name
		self.id = uuid.uuid1()
		self.creationTime = datetime.datetime.now()
		self.priority = ""
		self.petriNet = ""

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def getPriority(self):
		return self.priority

	def setPriority(self, priority):
		self.priority = priority

	def getCreationTime(self):
		return self.creationTime

	def getTimeSinceCreation():
		return datetime.datetime.now() - self.getCreationTime()

	def setPetriNet(self, petriNet):
		self.petriNet = petriNet

	def getPetriNet(self):
		return self.petriNet

	def setEntitySets(self, entitySet):
		self.entitySets.append(entitySet)

	def getEntitySets(self):
		return self.entitySets
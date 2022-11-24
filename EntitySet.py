from ModeTypesEnum import ModeTypes

class EntitySet(object):
	def __init__(self, name):
		self.entities = []
		self.name = name

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def getSize(self):
		return len(self.entities)

	def getMode(self):
		return self.mode

	def setMode(self, mode):
		self.mode = mode

	def getDuration(self):
		return self.duration

	def insert(self, entity): #TODO: consider the mode
		self.entities.append(entity)

	def pop(self): #TODO:consider the mode.
		return self.entities.pop(0)

	def removeEntityById(self, id):
		foundEntityIndex = -1
		for x, entity in enumerate(self.entities):
			if entity.getId() == id:
				foundEntityIndex = x

		if foundEntityIndex != -1:
			return self.entities.pop(foundEntityIndex)
		else:
			raise Exception('Unable to dequeue unqueued entity')

	def isEmpty(self):
		if len(self.entities) == 0:
			return True
		else:
			return False

	def isEntityInQueueById(self, id):
		foundEntityIndex = -1
		for x, entity in enumerate(self.entities):
			if entity.getId() == id:
				foundEntityIndex = x

		if foundEntityIndex != -1:
			return True
		else:
			return False
		pass

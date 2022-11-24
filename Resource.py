class Resource(object):
	def __init__(self, name, quantity):
		self.name = name
		self.quantity = quantity
		self.usedResources = 0
		self.id = ""

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def isAvailable(self):
		if self.usedResources < self.quantity:
			return True
		else:
			return False

	def allocate(self, quantity):
		if self.quantity == self.usedResources:
			return False
		else:
			self.usedResources += 1
			return True

	def release(self, quantity):
		if self.usedResources == 0:
			raise Exception('Não foi possível liberar recurso não alocado.')
		self.usedResources -= 1
		pass

	def getCurrentUsedResources(self):
		return self.usedResources

	def allocationRate(self):
		#TODO return percentual do tempo 
		# (em relação ao tempo total simulado) 
		# em que estes recursos foram alocados
		pass

	def averageAllocation(self):
		#TODO return quantidade média destes recursos que foram
		# alocados (em relação ao total simulado)
		pass

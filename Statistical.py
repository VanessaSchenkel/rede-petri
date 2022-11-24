import matplotlib.pyplot as plt

class Statistical(object):
	def __init__(self):
		self.resource_allocation = {}
		self.dict_statistics = {}
		self.queueSizes = {}

	def appendStatisticalData(self, time, resources, queues):
		self.__appendResourceAllocation__(time, resources)
		self.__appendQueueSizes__(time, queues)

	def __appendResourceAllocation__(self, time, resources):
		for key in resources:
			if key not in self.resource_allocation:
				self.resource_allocation[key] = {'x':[time], 'y':[resources[key].getCurrentUsedResources()]}
			else:
				self.resource_allocation[key]['x'].append(time)
				self.resource_allocation[key]['y'].append(resources[key].getCurrentUsedResources())

	def __appendQueueSizes__(self, time, queues):
		for key in queues:
			if key not in self.queueSizes:
				self.queueSizes[key] = {'x':[time], 'y':[queues[key].getSize()]}
			else:
				self.queueSizes[key]['x'].append(time)
				self.queueSizes[key]['y'].append(queues[key].getSize())


	def increaseDictLikeStatistic(self, key, increaseBy):
		if key not in self.dict_statistics:
			self.dict_statistics[key] = increaseBy
		else:
			self.dict_statistics[key] += increaseBy

	def __plotStatGraphs__(self):
		for key in self.resource_allocation:
			# print(self.resource_allocation[key])
			plt.plot(self.resource_allocation[key]['x'], self.resource_allocation[key]['y'])
			plt.xlabel('Tempo')
			plt.ylabel('Recursos')
			plt.title(key)
			plt.show()
		for key in self.queueSizes:
			# print("inisde a queue")
			# print(self.queueSizes[key])
			plt.plot(self.queueSizes[key]['x'], self.queueSizes[key]['y'])
			plt.xlabel('Tempo')
			plt.ylabel('Filas')
			plt.title(key)
			plt.show()

		

	def __printConsoleStatistics__(self):
		for key in self.dict_statistics:
			print(key + ":" + str(self.dict_statistics[key]))

	def displayStatistics(self):
		self.__printConsoleStatistics__()
		self.__plotStatGraphs__()
class ScheduledEvent(object):
	def __init__(self, time, event, args):
		self.scheduledTime = time
		self.event = event
		if args != {}:
			self.args = args
		else:
			self.args = None

	def getScheduledTime(self):
		return self.scheduledTime
from PySide2 import QtCore


class Thread(QtCore.QThread):
	failed = QtCore.Signal(Exception)
	successful = QtCore.Signal(object)

	def __init__(self, parent = None):
		super().__init__(parent)
		self.__func = None
		self.__looping = False
		self.__args = {}
		self.__resultQueue = []
		self.__resultQueueLimit = 10

	def run(self):
		firstIteration = True
		while self.__looping or firstIteration:
			firstIteration = False
			try:
				if self.__args:
					returnValue = self.__func(**self.__args)

				else:
					returnValue = self.__func()

			except Exception as e:
				self.failed.emit(e)
				return

			self.__resultQueue.append(returnValue)
			self.successful.emit(returnValue)

	def start(self, func = None, looping = False, **kwargs):
		if func:
			self.__func = func
		if kwargs:
			self.__args = kwargs
		if looping:
			self.__looping = bool(looping)
		super().start()

	def setFunction(self, func):
		self.__func = func

	def setArgs(self, **kwargs):
		self.__args = kwargs

	def setLooping(self, looping):
		self.__looping = bool(looping)

	def setResultQueueLimit(self, limit):
		self.__resultQueueLimit = int(limit)

	def getResult(self):
		return self.__resultQueue.pop(0)

	def breakLoop(self):
		self.__looping = False

	def resultQueueLimit(self):
		return self.__resultQueueLimit

	def addToResultQueue(self, value):
		if len(self.__resultQueue) == self.resultQueueLimit():
			self.__resultQueue.pop(0)

		self.__resultQueue.append(value)

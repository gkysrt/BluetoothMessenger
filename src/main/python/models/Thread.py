from PySide2 import QtCore


class Thread(QtCore.QThread):
	failed = QtCore.Signal(Exception)
	successful = QtCore.Signal(object)

	def __init__(self, parent = None):
		super().__init__(parent)
		self.__func = None
		self.__args = {}
		self.__resultQueue = []

	def run(self):
		try:
			if self.__args:
				returnValue = self.__func(**self.__args)

			else:
				returnValue = self.__func()

		except Exception as e:
			print("Thread failed:", str(e))
			self.failed.emit(e)
			return

		self.__resultQueue.append(returnValue)
		self.successful.emit(returnValue)

	def start(self, func = None, **kwargs):
		if func:
			self.__func = func
		if kwargs:
			self.__args = kwargs
		super().start()

	def setFunction(self, func):
		self.__func = func

	def setArgs(self, **kwargs):
		self.__args = kwargs

	def getResult(self):
		return self.__resultQueue.pop(0)
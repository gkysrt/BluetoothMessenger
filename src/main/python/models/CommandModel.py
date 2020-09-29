from PySide2 import QtCore


class CommandModel(QtCore.QObject):
	commandAdded = QtCore.Signal(object)
	commandRemoved = QtCore.Signal(object)
	commandReset = QtCore.Signal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.__cmdDict = {}

	def getCommands(self):
		return self.__cmdDict.keys()

	def setCommands(self, commandDict):
		self.resetCommands()
		self.__cmdDict = commandDict

	def getCommandNames(self):
		return [cmd.name() for cmd in self.__cmdDict.values()]

	def addCommand(self, cmd):
		self.__cmdDict[cmd.command()] = cmd
		self.commandAdded.emit(cmd)

	def resetCommands(self):
		self.__cmdDict = {}
		self.commandReset.emit()

	def removeCommand(self, cmd):
		self.__cmdDict.pop(cmd.command())
		self.commandRemoved.emit(cmd)

	def getCommand(self, key):
		return self.__cmdDict.get(key)

	def getCommandDict(self):
		return self.__cmdDict

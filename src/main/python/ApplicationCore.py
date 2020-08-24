# ApplicationCore is the application context itself (inherited) with added functionality of path providing
# and also designed to be Singleton

from fbs_runtime.application_context.PySide2 import ApplicationContext
from fbs_runtime.application_context import is_frozen
import os


class ApplicationCore(ApplicationContext):
	__instance = None

	def __init__(self):
		super(ApplicationCore, self).__init__()

		if self.__instance is not None:
			raise RuntimeError("ApplicationCore is a singleton object, use getInstance() method instead")
		else:
			ApplicationCore.__instance = self

	def getIcon(self, icon = ''):
		return self.get_resource(os.path.join('icons'), icon)

	def getQss(self, qss = ''):
		return self.get_resource(os.path.join('qss'), qss)

	def getQml(self, qml = ''):
		return self.get_resource(os.path.join('qml'), qml)

	def getPlugin(self, plugin = ''):
		return self.get_resource(os.path.join('plugins'), plugin)

	# def getCommand(self, command = ''):
		# Should match case names be given?
		# commandName = command.upper()
		# commandName = commandName + ".py" if not commandName.endswith('.PY', -3) else commandName

	def pluginPath(self):
		return self.get_resource('plugins')

	def qssPath(self):
		return self.get_resource('qss')

	def qmlPath(self):
		return self.get_resource('qml')

	def iconPath(self):
		return self.get_resource('icons')

	def isFrozen(self):
		return is_frozen()

	def getApplicationPalette(self):
		return

	@staticmethod
	def getInstance():
		if ApplicationCore.__instance is None:
			ApplicationCore()

		return ApplicationCore.__instance


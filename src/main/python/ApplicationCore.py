# ApplicationCore is the application context itself (inherited) with added functionality of path providing
# and also designed to be Singleton

from fbs_runtime.application_context.PySide2 import ApplicationContext
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

	def getPlugin(self, plugin = ''):
		return self.get_resource(os.path.join('plugins'), plugin)

	def pluginPath(self):
		return self.get_resource('plugins')

	def qssPath(self):
		return self.get_resource('qss')

	def iconPath(self):
		return self.get_resource('icons')

	@staticmethod
	def getInstance():
		if ApplicationCore.__instance is None:
			ApplicationCore()

		return ApplicationCore.__instance

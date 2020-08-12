import os
import importlib
import BaseCommand


# Class designed to read files convenient for plugin structure
# Class name should be "class Plugin()"

class PluginReader(object):
	def __init__(self):
		super(PluginReader, self).__init__()
		self.__cmdDict = dict()

	# Searches for possible plugins and stores them dict
	def loadCommands(self):
		# Search for files that may be plug-ins on predefined directory
		print(self.COMMANDS_DIRECTORY)
		for file in os.listdir(self.COMMANDS_DIRECTORY):
			name, extension = os.path.splitext(file)

			if extension == ".py":
				module = importlib.import_module(self.COMMANDS_PACKAGE + ".%s" % name)
				instance = self.pluginInstance(module)
				self.__cmdDict[instance.command()] = instance

	# Creates instance of plugin class inside given module
	def pluginInstance(self, module):
		pluginClass = None

		try:
			pluginClass = module.Command

		except AttributeError as e:
			print("Error creating exporter plugin objects, {} - {}".format(module, str(e)))

		if issubclass(pluginClass, BaseCommand.BaseCommand):
			pluginInstance = pluginClass()
			return pluginInstance

		else:
			return None

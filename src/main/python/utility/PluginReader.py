import os
import importlib
from BaseCommand import BaseCommand

# Class designed to read files convenient for plugin structure
# Class name should be "class Plugin()"
from ApplicationCore import ApplicationCore


class PluginReader(object):
	def __init__(self):
		super(PluginReader, self).__init__()

	# Loads plugins in given package and path and returns them in a dict
	# e.g usage loadPlugins("plugins.commands", os.path.join('plugins', 'commands'))
	@staticmethod
	def loadPlugins(pluginPackage, pluginDirectory, pluginParentClass = None):
		pluginDict = {}
		print("pluginParentClass", pluginParentClass)
		# Search for files that may be plug-ins on given directory
		for file in os.listdir(pluginDirectory):
			name, extension = os.path.splitext(file)
			if extension == ".py":
				module = importlib.import_module(pluginPackage + ".%s" % name)
				instance = PluginReader.pluginInstance(module, pluginParentClass)
				if instance:
					pluginDict[instance.command()] = instance

		return pluginDict

	"""
	:parameter 
		module -> Module to search for plugins, str
		pluginParentClass -> Parent class that is designed to be parent of plugins. If pluginParentClass is None no parent
		condition is looked for
	:return
		instance of plugin object
	
	Creates instance of plugin class inside given module and returns it
	
	"""
	@staticmethod
	def pluginInstance(module, pluginParentClass = None):
		pluginClass = None

		try:
			pluginClass = module.Plugin

		except AttributeError as e:
			print("Error creating exporter plugin objects, {} - {}".format(module, str(e)))
			return None

		if pluginClass and pluginParentClass and issubclass(pluginClass, pluginParentClass):
			pluginInstance = pluginClass()
			return pluginInstance

		else:
			return None

import os
import importlib
import BaseCommand


class CommandParser(object):

	COMMANDS_DIRECTORY = os.path.join(os.path.curdir, "commands")
	COMMANDS_PACKAGE = "commands"

	def __init__(self, name = None):
		self.__programName = name
		self.__cmdDict = dict()
		self.loadCommands()

	# This method parses argument and executes related command with given kwargs
	def parse(self, argumentString, **kwargs):
		# If user typed in no specific command
		if argumentString == "help" or argumentString == "info":
			self.displayManual()
			return

		elif argumentString == "clear":
			os.system('clear')
			return

		elif argumentString == "":
			return

		argumentList = argumentString.split()

		# First argument is always the command, rest are the arguments, options etc.
		# Command is removed from argumentList
		commandString = argumentList.pop(0)

		if commandString in self.__cmdDict.keys():
			command = self.__cmdDict.get(commandString)
			return command.execute(argumentList, ** kwargs)

		else:
			print("Command not recognized. Type \"help\" to display manual.")

	# Searches for possible plugins and stores them dict
	def loadCommands(self):
		# Search for files that may be plug-ins on predefined directory
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

	# Prints out all available commands' info
	def displayManual(self):
		for command in self.__cmdDict.values():
			print(command.info())

# An example command implementation takes place below. You can use it to understand how to add a command to the program.
# Commands are implemented in a plugin fashion, every time a file inherits BaseCommand inside /commands file,
# it'll be added and evaluated as an argument
# You can uncomment below lines to add an ExampleCommand

# from PySide2 import QtWidgets, QtCore
# import BaseCommand
#
#
# class Plugin(BaseCommand.BaseCommand):
# 	__options = ("-h", "-c")
# 	__cmd = "example-command"
# 	__name = "Example Command"
#
# 	def __init__(self, parent = None):
# 		super().__init__(parent)
#
# 	@classmethod
# 	def options(cls):
# 		"""
# 		:param
# 		:return set
# 		options() function simply returns available options in type tuple.
# 		e.g tuple("-v", "-h", "-t")
# 		Returned set is used for displaying in manual and also crucial for predefining available options
# 		"""
# 		return cls.__options
#
# 	@classmethod
# 	def command(cls):
# 		"""
# 		:param
# 		:return str
# 		command() function simply returns a distinct name for the argument to use.
# 		command() is used for comparing user input to command.
# 		class inheriting BaseCommand must implement this method.
# 		"""
# 		return cls.__cmd
#
#
# 	@classmethod
# 	def name(cls):
# 		"""
# 		:param
# 		:return str
# 		name() function should simply return the name of plugin that'll be shown on display of UI.
# 		Override this function and return a string to name your command on UI.
# 		If not reimplemented, name will be blank.
# 		"""
# 		return cls.__name
#
# 	@staticmethod
# 	def info():
# 		"""
# 		:param
# 		:return str
# 		info() function simply returns a description for the argument.
# 		This is optional.
# 		"""
# 		return """example-command [options]: Example command
# 				OPTIONS:
# 					-h / --help: Show help"""
#
# 	def setupUi(self):
# 		"""
# 		:param
# 		:return
# 		A free space is given inside command panel widget to override setupUi() method and fill free space.
# 		This way, visualization of plugin part is fully customizable. You can take inputs from user and
# 		use the given space freely. If setupUi() is not overridden and reimplemented, command will not be added
# 		to UI
# 		"""
# 		layout = QtWidgets.QVBoxLayout(self)
#
# 		textLabel = QtWidgets.QLabel(self)
# 		textLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
# 		textLabel.setText("Example Command")
# 		textLabel.setAlignment(QtCore.Qt.AlignCenter)
# 		layout.addWidget(textLabel)
#
# 	def execute(self, argList, **kwargs):
# 		"""
# 		:param list
# 		:return dict
# 		execute() function does what argument should do upon execution.
# 		argList is a list of strings, and it is in order which user typed in .
# 		String list is parsed string list of user input and sent by CommandParser.
# 		Default return type is dict.
# 		e.g
# 			return {"command": self.command(), "result": "successful", "devices": list(nearbyDevices)}
#
# 		"""
# 		print("Example Command")
# 		return {"command": self.command(), "result": "successful"}
#
# 	def executeUI(self, **kwargs):
# 		"""
# 		:param kwargs:
# 		:return:
# 		execute() function does what command should do upon execution, <u><b>from UI</b></u>.
# 		Default return type is dict.
# 		If this method is not overridden an implemented, it will be a blank command on UI
# 		e.g
# 			return {"command": self.command(), "result": "successful", "devices": list(nearbyDevices)}
# 		"""
# 		QtWidgets.QMessageBox.information(self.parent(), "Example Command", "You executed example command!", QtWidgets.QMessageBox.Ok)
# 		return {'command': self.command(), 'result': 'successful'}
#
# 	def isDisplayed(self):
# 		"""
# 		:param :
# 		:return: bool
# 		This function simply returns if command should be on display (CommandPanel) or not. Override this function and
# 		set return value as False to cancel display of command.
# 		"""
# 		return True

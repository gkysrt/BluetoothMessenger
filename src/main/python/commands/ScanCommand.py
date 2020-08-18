import BaseCommand
import bluetooth


class Plugin(BaseCommand.BaseCommand):
	def __init__(self, parent=None):
		super().__init__(parent)

	__options = ("-h", "--help", "-f", "--flush", "-d", "--duration", "-c", "--class", "-h", "--help")
	__cmd = "scan"
	__name = "Scan"

	@classmethod
	def options(cls):
		return cls.__options

	@classmethod
	def command(cls):
		return cls.__cmd

	@classmethod
	def name(cls):
		return cls.__name

	@staticmethod
	def info():
		return """scan [options]: Scan area for available bluetooth devices
		OPTIONS:
			-n / --name : Show names
			-f / --flush: Flush cache
			-d / --duration: Timeout duration (Default 8sec)
			-c / --class : Show lookup class
			-h / --help : Show help
		e.g:
			scan -d 4 -f -n -c
			"""

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.command(), "result": "failed"}

		print("Starting bluetooth scan..")

		namesEnabled = False
		flushCache = False
		lookupClass = False
		duration = 8

		if '-f' in argList or "--flush" in argList:
			flushCache = True

		if "-c" in argList or "--class" in argList:
			lookupClass = True

		if "-n" in argList or "--name" in argList:
			namesEnabled = True

		for i in range(len(argList)):
			if argList[i] == "-d" or argList[i] == "--duration":
				if 4 < int(argList[i + 1]) < 32:
					duration = int(argList[i + 1])

		try:
			nearbyDevices = bluetooth.discover_devices(lookup_names=namesEnabled, flush_cache=flushCache,
													   lookup_class=lookupClass, duration=duration)

		except Exception as e:
			print("Failed to bluetooth scan nearby devices", str(e))
			return {"command": self.command(), "result": "failed"}

		for device in nearbyDevices:
			print(device)
		print("Found {} devices.".format(len(nearbyDevices)))

		return {"command": self.command(), "result": "successful"}

	def executeUI(self, **kwargs):
		namesEnabled = True
		flushCache = True
		lookupClass = True
		duration = 8

		print("Starting bluetooth scan..")

		try:
			nearbyDevices = bluetooth.discover_devices(lookup_names=namesEnabled, flush_cache=flushCache,
													   lookup_class=lookupClass, duration=duration)
		except Exception as e:
			print("Failed to bluetooth scan nearby devices", str(e))
			return {"command": self.command(), "result": "failed"}

		print("Found {} devices.".format(len(nearbyDevices)))
		return {"command": self.command(), "result": "successful", "devices": list(nearbyDevices)}

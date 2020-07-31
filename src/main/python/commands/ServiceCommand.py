import BaseCommand
import bluetooth


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "--help", "-u", "--uuid", "-n", "--name", "-m", "--mac")
	cmd = "service"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

	@staticmethod
	def info():
		return """service [options]: Scan target uuid, mac and name for its available services
			OPTIONS:
				-u / --uuid : UUID input for target
				-n / --name: Name input for target
				-m / --mac: MAC address input for target
				-h / --help : Show help

			e.g:
				service -u 24345-691df-120g5lf -n evc04 -m 34:1G:33:12:66:00
			"""

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.cmd, "result": "failed"}
		print("Looking for target services..")

		name = None
		mac = None
		uuid = None

		for i in range(len(argList)):
			if "-u" == argList[i] or "--uuid" == argList[i]:
				if argList[i+1]:
					uuid = argList[i+1]
					continue

			elif "-m" == argList[i] or "--mac" == argList[i]:
				if argList[i+1]:
					mac = argList[i+1]
					continue

			elif "-n" == argList[i] or "--name" == argList[i]:
				if argList[i+1]:
					name = argList[i+1]
					continue

		if name is None and mac is None and uuid is None:
			print("You must at least specify one option for the target")
			return {"command": self.cmd, "result": "failed"}

		try:
			serviceList = bluetooth.find_service(address=mac, uuid=uuid, name=name)

		except Exception as e:
			print("Error finding services %s" % str(e))
			return {"command": self.cmd, "result": "failed"}

		print("Service scan is completed")
		for service in serviceList:
			print(service)

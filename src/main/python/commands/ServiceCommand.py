import BaseCommand
import bluetooth


class Plugin(BaseCommand.BaseCommand):
	def __init__(self, parent=None):
		super().__init__(parent)

	__options = ("-u", "--uuid", "-n", "--name", "-m", "--mac")
	__cmd = "service"
	__name = "Scan Service"

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
		return """service [options]: Scan target uuid, mac and name for its available services
		OPTIONS:
			-u / --uuid: UUID input for target
			-n / --name: Name input for target
			-m / --mac: MAC address inpıt for target
		e.g:
			service -u 24345-591df-12043 -n evc04 -m 34:1F:33:12:66:AC"""

	def execute(self, argList, **kwargs):
		print("Looking for target services..")

		name = None
		mac = None
		uuid = None

		for i in range(len(argList)):
			if "-u" == argList[i] or "--uuid" == argList[i]:
				if argList[i + 1]:
					uuid = argList[i + 1]
					continue

			elif "-m" == argList[i] or "--mac" == argList[i]:
				if argList[i + 1]:
					mac = argList[i + 1]
					continue

			elif "-n" == argList[i] or "--name" == argList[i]:
				if argList[i + 1]:
					name = argList[i + 1]
					continue

		if name is None and mac is None and uuid is None:
			print("You must at least specify one option for the target")
			return {"command": self.command(), "result": "failed"}

		try:
			serviceList = bluetooth.find_service(address=mac, uuid=uuid, name=name)

		except Exception as e:
			print("Error finding services %s" % str(e))
			return {"command": self.command(), "result": "failed"}

		print("Service scan is completed")
		for service in serviceList:
			print(service)

		return {"command": self.command(), "result": "successful", "services": list(serviceList)}

	def executeUI(self, **kwargs):

		name = kwargs.get('name', None)
		mac = kwargs.get('mac', None)
		uuid = kwargs.get('uuid', None)
		print("Looking for target services..")

		if name is None and mac is None and uuid is None:
			print("You must at least specify one option for the target")
			return {"command": self.command(), "result": "failed"}

		try:
			serviceList = bluetooth.find_service(address=mac, uuid=uuid, name=name)

		except Exception as e:
			print("Error finding services %s" % str(e))
			return {"command": self.command(), "result": "failed"}

		print("Service scan is completed")
		for service in serviceList:
			print(service)

		return {"command": self.command(), "result": "successful", "services": list(serviceList)}

	def isDisplayed(self):
		return False

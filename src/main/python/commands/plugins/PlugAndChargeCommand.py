import json
import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	__options = ("-h", "--help", "-c", "--connector")
	__cmd = "plug-and-charge"
	__name = "Plug and Charge"

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
		return """lockable-cable [on/off] [options]: Plug and charge command, used with on/off arguments
		OPTIONS:
			-h / --help: Show help
            -c / --connector: Specify a connector ID (default connector ID is 1)
        e.g
            plug-and-charge on -c 1
		"""

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.command(), "result": "failed"}

		onOffArgument = argList.pop(0)
		connectorID = 1

		for i in range(len(argList)):
			if "-c" == argList[i] or "--connector" == argList[i]:
				if argList[i + 1]:
					connectorID = int(argList[i + 1])
					

		socket = kwargs.get('socket')
		print("Requesting lockable cable: ", onOffArgument)

		try:
			if onOffArgument == "off":
				lockableCableRequest = {"chargePoints": [{"connectorId": connectorID, "settings": [
					{"key": "Charger.EVC.Setting.PlugAndCharge", "value": False}]}]}

				socket.send(json.dumps(lockableCableRequest).encode())
				return {"command": self.command(), "result": "successful"}

			elif onOffArgument == "on":
				lockableCableRequest = {
					"chargePoints": [{
						"connectorId": connectorID,
						"settings": [{
							"key": "Charger.EVC.Setting.PlugAndCharge",
							"value": True
						}]
					}]
				}
				socket.send(json.dumps(lockableCableRequest).encode())
				print("Lockable cable is successfully requested: {}".format(onOffArgument))
				return {"command": self.command(), "result": "successful"}

			else:
				raise Exception("Second argument should be on/off")

		except Exception as e:
			print("Failed to send lockable-cable request: %s" % str(e))
			return {"command": self.command(), "result": "failed"}

	def executeUI(self, **kwargs):
		onOffArgument = "ON"
		connectorID = 1

		socket = kwargs.get('socket')
		print("Requesting lockable cable: ", onOffArgument)

		try:
			if onOffArgument == "off":
				lockableCableRequest = {"chargePoints": [{"connectorId": connectorID, "settings": [
					{"key": "Charger.EVC.Setting.PlugAndCharge", "value": False}]}]}

				socket.send(json.dumps(lockableCableRequest).encode())
				return {"command": self.command(), "result": "successful"}

			elif onOffArgument == "on":
				lockableCableRequest = {
					"chargePoints": [{
						"connectorId": connectorID,
						"settings": [{
							"key": "Charger.EVC.Setting.PlugAndCharge",
							"value": True
						}]
					}]
				}
				socket.send(json.dumps(lockableCableRequest).encode())
				print("Lockable cable is successfully requested: {}".format(onOffArgument))
				return {"command": self.command(), "result": "successful"}

			else:
				raise Exception("Second argument should be on/off")

		except Exception as e:
			print("Failed to send lockable-cable request: %s" % str(e))
			return {"command": self.command(), "result": "failed"}

	def setupUi(self):
		pass

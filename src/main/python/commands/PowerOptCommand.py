import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "--help")
	cmd = "power-optimizer"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

	@staticmethod
	def info():
		return """power-optimizer [on/off] [options]: Power optimizer command
            OPTIONS:
                -h / --help : Show help
            """

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.cmd, "result": "failed"}

		connectorID = 1
		for i in range(len(argList)):
			if "-c" == argList[i] or "--connector" == argList[i]:
				if argList[i + 1]:
					connectorID = argList[i + 1]
		socket = kwargs.get('socket')
		optimizerEnabled = argList.pop(0)

		print("Requesting power optimizer: ", optimizerEnabled)

		if optimizerEnabled == "on":
			value = "true"
		elif optimizerEnabled == "off":
			value = "false"
		else:
			print('Second argument must be "on" or "off"')
			return {"command": self.cmd, "result": "failed"}

		powerOptimizerRequest = {
			"chargePoints": [{
				"connectorId": connectorID,
				"programs": [{
					"key": "Charger.EVC.Program.PowerOptimizer",
					"value": value
				}],
			}]
		}

		try:
			socket.send(json.dumps(powerOptimizerRequest).encode())
			print("Power optimizer is requested: connectorID {}".format(str(connectorID)))
			return {"command": self.cmd, "result": "successful"}

		except Exception as e:
			print("Failed to request power optimizer: ", optimizerEnabled + " - ", str(e))
			return {"command": self.cmd, "result": "failed"}


import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "-c", "--connector", "--help")
	cmd = "stop-charge"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

	@staticmethod
	def info():
		return """stop-charge [options]: Stop charge command, used to signal the end of the charging.  
            OPTIONS:
                -h / --help : Show help
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                stop-charge --connector 1
            """

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.cmd, "result": "failed"}

		socket = kwargs.get('socket')
		print("Requesting stop charge")

		connectorID = 1
		for i in range(len(argList)):
			if argList[i] == "-c" or argList[i] == "--connector":
				if argList[i + 1]:
					connectorID = argList[i + 1]

		stopRequest = {"chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Stop"}]}]}

		try:
			socket.send(json.dumps(stopRequest).encode())

		except Exception as e:
			print("Failed to send stop-charge request", str(e))
			return {"command": self.cmd, "result": "failed"}

		print("Stop charge is successfully requested: connectorID {}".format(str(connectorID)))
		return {"command": self.cmd, "result": "successful"}

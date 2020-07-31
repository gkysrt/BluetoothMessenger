import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "--help")
	cmd = "reconfigure"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

	@staticmethod
	def info():
		return """reconfigure [options]: Master reconfigure command, used to reconfigure.
            OPTIONS:
                -h / --help : Show help
            e.g
                reconfigure
            """

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.cmd, "result": "failed"}

		socket = kwargs.get('socket')
		print("Requesting master reconfigure")

		reconfigureRequest = {
			"chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.MasterReconfigure"}]}]}
		try:
			socket.send(json.dumps(reconfigureRequest).encode())

		except Exception as e:
			print("Failed to send reconfiguration request", str(e))
			return {"command": self.cmd, "result": "failed"}

		print("Master reconfiguration is successfully requested")
		return {"command": self.cmd, "result": "successful"}

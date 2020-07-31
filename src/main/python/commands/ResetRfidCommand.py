import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "--help")
	cmd = "reset-rfid"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

	@staticmethod
	def info():
		return """reset-rfid [options]: User card reset command.
            OPTIONS:
                -h / --help : Show help
            """

	def execute(self, argList, **kwargs):
		if '-h' in argList or '--help' in argList:
			print(self.info())
			return {"command": self.cmd, "result": "failed"}

		socket = kwargs.get('socket')
		print("Requesting user card reset")

		userCardResetRequest = {
			"chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.UserCardReset"}]}]}
		try:
			socket.send(json.dumps(userCardResetRequest).encode())

		except Exception as e:
			print("Failed to send user card reset request", str(e))
			return {"command": self.cmd, "result": "failed"}

		print("User card reset is successfully requested")
		return {"command": self.cmd, "result": "successful"}

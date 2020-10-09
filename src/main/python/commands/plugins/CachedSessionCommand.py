import BaseCommand
import json


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	__options = ()
	__cmd = "cached-session"
	__name = "Cached Session"

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
		return """cached-session [date] [options]: Cached Session Request command, used to request a cached session. cached-session keyword is followed by a date in epoch format.
			OPTIONS:
				-
			e.g:
				cached-session 791404523
			"""

	def execute(self, argList, **kwargs):
		socket = kwargs.get('socket')
		print("Requesting cached session..")

		dateString = argList.pop(0)

		cachedSessionRequest = {
			"MessageType": "CachedSessionRequest",
			"Date": str(dateString)
		}

		try:
			socket.send(json.dumps(cachedSessionRequest).encode())

		except Exception as e:
			print("Failed to send cached session message to peer ", str(e))
			return {"command": Command.command(), "result": "failed"}

		print("Cached session request is successfully sent to peer")
		return {"command": Command.command(), "result": "successful"}

	def executeUI(self, **kwargs):
		socket = kwargs.get('socket')
		print("Requesting cached session..")

		dateString = "5983401" 	# Epoch date string

		cachedSessionRequest = {
			"MessageType": "CachedSessionRequest",
			"Date": str(dateString)
		}

		try:
			socket.send(json.dumps(cachedSessionRequest).encode())

		except Exception as e:
			print("Failed to send cached session message to peer ", str(e))
			return {"command": Command.command(), "result": "failed"}

		print("Cached session request is successfully sent to peer")
		return {"command": Command.command(), "result": "successful"}

	def setupUi(self):
		pass
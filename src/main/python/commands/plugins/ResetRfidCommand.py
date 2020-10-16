import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ()
    __cmd = "reset-rfid"
    __name = "Reset RFID"

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
        return """reset-rfid [options]: User card reset command.
            OPTIONS:
                -"""

    def execute(self, argList, **kwargs):
        socket = kwargs.get('socket')
        print("Requesting user card reset")

        userCardResetRequest = {
            "chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.UserCardReset"}]}]}
        try:
            socket.send(json.dumps(userCardResetRequest).encode())

        except Exception as e:
            print("Failed to send user card reset request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("User card reset is successfully requested")
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')
        print("Requesting user card reset")

        userCardResetRequest = {
            "chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.UserCardReset"}]}]}
        try:
            socket.send(json.dumps(userCardResetRequest).encode())

        except Exception as e:
            print("Failed to send user card reset request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("User card reset is successfully requested")
        return {"command": self.command(), "result": "successful"}

    def setupUi(self):
        pass
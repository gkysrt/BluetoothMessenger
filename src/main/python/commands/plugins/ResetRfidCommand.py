import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-h", "--help")
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
                -h / --help : Show help
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

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

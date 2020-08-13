import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-h", "--help")
    __cmd = "reconfigure"
    __name = "Reconfigure"

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
        return """reconfigure [options]: Master reconfigure command, used to reconfigure.
            OPTIONS:
                -h / --help : Show help
            e.g
                reconfigure
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        socket = kwargs.get('socket')
        print("Requesting master reconfigure")

        reconfigureRequest = {
            "chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.MasterReconfigure"}]}]}
        try:
            socket.send(json.dumps(reconfigureRequest).encode())

        except Exception as e:
            print("Failed to send reconfiguration request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Master reconfiguration is successfully requested")
        return {"command": self.command(), "result": "successful"}

import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-c", "--connector")
    __cmd = "pause-charge"
    __name = "Pause"

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
        return """pause-charge [options]: Pause charge command, pauses ongoing charging.
            OPTIONS:
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                pause-charge -c 1"""

    def execute(self, argList, **kwargs):
        socket = kwargs.get('socket')
        print("Requesting pause charge")

        connectorID = 1
        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        pauseRequest = {
            "chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Pause"}]}]}

        try:
            socket.send(json.dumps(pauseRequest).encode())
            print("Pause charge is successfully requested: connectorID {}".format(str(connectorID)))

        except Exception as e:
            print("Failed to send pause-charge request", str(e))
            return {"command": self.command(), "result": "failed"}

        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')
        print("Requesting pause charge")

        connectorID = 1
        pauseRequest = {
            "chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Pause"}]}]}

        try:
            socket.send(json.dumps(pauseRequest).encode())
            print("Pause charge is successfully requested: connectorID {}".format(str(connectorID)))

        except Exception as e:
            print("Failed to send pause-charge request", str(e))
            return {"command": self.command(), "result": "failed"}

        return {"command": self.command(), "result": "successful"}

    def isDisplayed(self):
        return False

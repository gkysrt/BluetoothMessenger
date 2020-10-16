import json

import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-c", "--connector")
    __cmd = "stop-charge"
    __name = "Stop"

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
        return """stop-charge [options]: Stop charge command, used to signal the end of the charging.  
            OPTIONS:
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                stop-charge --connector 1"""

    def execute(self, argList, **kwargs):
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
            return {"command": self.command(), "result": "failed"}

        print("Stop charge is successfully requested: connectorID {}".format(str(connectorID)))
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')
        print("Requesting stop charge")

        connectorID = 1
        stopRequest = {"chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Stop"}]}]}

        try:
            socket.send(json.dumps(stopRequest).encode())

        except Exception as e:
            print("Failed to send stop-charge request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Stop charge is successfully requested: connectorID {}".format(str(connectorID)))
        return {"command": self.command(), "result": "successful"}

    def isDisplayed(self):
        return False

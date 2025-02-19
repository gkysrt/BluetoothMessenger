import json

import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-c", "--connector")
    __cmd = "start-charge"
    __name = "Start"

    @classmethod
    def options(cls):
        return cls.__options

    @classmethod
    def name(cls):
        return cls.__name

    @classmethod
    def command(cls):
        return cls.__cmd

    @staticmethod
    def info():
        return """start-charge [options]: Start charge command, used to signal the start of charging.
            OPTIONS:
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                start-charge --connector 1"""

    def execute(self, argList, **kwargs):
        socket = kwargs.get('socket')

        print("Requesting start charge")

        connectorID = 1
        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        startRequest = {
            "chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Start"}]}]}

        try:
            socket.send(json.dumps(startRequest).encode())

        except Exception as e:
            print("Failed to send start-charge request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Start charge is successfully requested: connectorID {}".format(str(connectorID)))
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')

        print("Requesting start charge")

        connectorID = 1
        startRequest = {
            "chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Start"}]}]}

        try:
            socket.send(json.dumps(startRequest).encode())

        except Exception as e:
            print("Failed to send start-charge request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Start charge is successfully requested: connectorID {}".format(str(connectorID)))
        return {"command": self.command(), "result": "successful"}

    def isDisplayed(self):
        return False

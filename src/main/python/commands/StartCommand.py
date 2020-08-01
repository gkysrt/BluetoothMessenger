import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "-c", "--connector", "--help")
    cmd = "start-charge"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

    @staticmethod
    def info():
        return """start-charge [options]: Start charge command, used to signal the start of charging.
            OPTIONS:
                -h / --help : Show help
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                start-charge --connector 1
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.cmd, "result": "failed"}

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
            return {"command": self.cmd, "result": "failed"}

        print("Start charge is successfully requested: connectorID {}".format(str(connectorID)))
        return {"command": self.cmd, "result": "successful"}

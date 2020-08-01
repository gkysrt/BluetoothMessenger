import json

import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "-c", "--connector", "--help")
    cmd = "resume-charge"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

    @staticmethod
    def info():
        return """resume-charge [options]: Resume charge command, used to resume a paused charging status.
            OPTIONS:
                -h / --help : Show help
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                resume-charge -c 1
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.cmd, "result": "failed"}

        socket = kwargs.get('socket')
        print("Requesting resume charge")

        connectorID = 1
        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        resumeRequest = {
            "chargePoints": [{"connectorId": connectorID, "command": [{"key": "Charger.EVC.Command.Resume"}]}]}
        print("Resume charge is successfully requested: connectorID {}".format(str(connectorID)))

        try:
            socket.send(json.dumps(resumeRequest).encode())

        except Exception as e:
            print("Failed to send start-charge request", str(e))
            return {"command": self.cmd, "result": "failed"}

        return {"command": self.cmd, "result": "successful"}

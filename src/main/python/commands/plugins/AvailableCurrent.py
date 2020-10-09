import json
import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    __options = ()
    __cmd = "available-current"
    __name = "Available Current"

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
        return """available-current [value] [options]: Available current command, takes integer value
            OPTIONS:
                -c / --connector: Specify a connector ID (default connector ID is 1)
            e.g
                available-current 7 -c 1
            """

    def execute(self, argList, **kwargs):
        connectorID = 1
        for i in range(len(argList)):
            if "-c" == argList[i] or "--connector" == argList[i]:
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        socket = kwargs.get('socket')
        value = int(argList.pop(0))

        print("Requesting available current change: ", value)

        availableCurrent = {
            "chargePoints": [{
                "connectorId": connectorID,
                "settings": [{
                    "key": "Charger.EVC.Setting.AvailableCurrent",
                    "value": value
                }],
            }]
        }

        try:
            socket.send(json.dumps(availableCurrent).encode())
            print("Available current change requested: connectorID {}".format(str(connectorID)))
            return {"command": self.command(), "result": "successful"}

        except Exception as e:
            print("Failed to request available current change: ", value + " - ", str(e))
            return {"command": self.command(), "result": "failed"}

    def executeUI(self, **kwargs):
        connectorID = 1
        socket = kwargs.get('socket')
        value = 5 # Integer current value

        print("Requesting available current change: ", value)

        availableCurrent = {
            "chargePoints": [{
                "connectorId": connectorID,
                "settings": [{
                    "key": "Charger.EVC.Setting.AvailableCurrent",
                    "value": value
                }],
            }]
        }

        try:
            socket.send(json.dumps(availableCurrent).encode())
            print("Available current change requested: connectorID {}".format(str(connectorID)))
            return {"command": self.command(), "result": "successful"}

        except Exception as e:
            print("Failed to request available current change: ", value + " - ", str(e))
            return {"command": self.command(), "result": "failed"}

    def setupUi(self):
        pass

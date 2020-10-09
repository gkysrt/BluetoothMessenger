import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ()
    __cmd = "power-optimizer"
    __name = "Power Optimizer"

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
        return """power-optimizer [on/off] [options]: Power optimizer command
            OPTIONS:
                -
            """

    def execute(self, argList, **kwargs):
        connectorID = 1
        for i in range(len(argList)):
            if "-c" == argList[i] or "--connector" == argList[i]:
                if argList[i + 1]:
                    connectorID = argList[i + 1]
        socket = kwargs.get('socket')
        optimizerEnabled = argList.pop(0)

        print("Requesting power optimizer: ", optimizerEnabled)

        if optimizerEnabled == "on":
            value = "true"
        elif optimizerEnabled == "off":
            value = "false"
        else:
            print('Second argument must be "on" or "off"')
            return {"command": self.command(), "result": "failed"}

        powerOptimizerRequest = {
            "chargePoints": [{
                "connectorId": connectorID,
                "programs": [{
                    "key": "Charger.EVC.Program.PowerOptimizer",
                    "value": value
                }],
            }]
        }

        try:
            socket.send(json.dumps(powerOptimizerRequest).encode())
            print("Power optimizer is requested: connectorID {}".format(str(connectorID)))
            return {"command": self.command(), "result": "successful"}

        except Exception as e:
            print("Failed to request power optimizer: ", optimizerEnabled + " - ", str(e))
            return {"command": self.command(), "result": "failed"}


    def executeUI(self, **kwargs):
        connectorID = 1

        socket = kwargs.get('socket')
        optimizerEnabled = "ON"

        print("Requesting power optimizer: ", optimizerEnabled)

        if optimizerEnabled.lower() == "on":
            value = "true"
        elif optimizerEnabled.lower() == "off":
            value = "false"
        else:
            print('Second argument must be "on" or "off"')
            return {"command": self.command(), "result": "failed"}

        powerOptimizerRequest = {
            "chargePoints": [{
                "connectorId": connectorID,
                "programs": [{
                    "key": "Charger.EVC.Program.PowerOptimizer",
                    "value": value
                }],
            }]
        }

        try:
            socket.send(json.dumps(powerOptimizerRequest).encode())
            print("Power optimizer is requested: connectorID {}".format(str(connectorID)))
            return {"command": self.command(), "result": "successful"}

        except Exception as e:
            print("Failed to request power optimizer: ", optimizerEnabled + " - ", str(e))
            return {"command": self.command(), "result": "failed"}

    def setupUi(self):
        pass

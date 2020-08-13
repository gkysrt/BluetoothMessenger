import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    __options = ("-h", "-c", "-s", "-m", "-h", "--second", "--minute", "--hour", "--connector", "--help")
    __cmd = "delay-charge"
    __name = "Delay Charge"

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
        return """delay-charge [on/off] [options]: Delay charge command, second arg on off, a delay amount should be specified
            OPTIONS:
                -h / --help: Show help
                -c / --connector: Connector ID (default connector ID is 1)
                -s / --second: Delay amount in seconds
                -m / --minute: Delay amount in minutes
                -h / --hour: Delay amount in hours
            e.g:
                delay-charge on -m 60 -c 1
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        delayEnabled = argList.pop(0)

        socket = kwargs.get('socket')
        connectorID = 1

        delayTime = 0
        timeUnit = "minute"

        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        for i in range(len(argList)):
            if argList[i] == "-m" or argList[i] == "--minute":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    break

            elif argList[i] == "-h" or argList[i] == "--hour":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    delayTime = delayTime * 60
                    # timeUnit = "hour"
                    break

            elif argList[i] == "-s" or argList[i] == "--second":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    # timeUnit = "second"
                    delayTime = delayTime / 60
                    break

        delayChargeRequest = None

        if delayEnabled == "on":
            # TODO: What is step, unit, min, max scale
            delayChargeRequest = {"chargePoints":
                [{
                    "connectorId": connectorID,
                    "programs":
                        [{"key": "Charger.EVC.Program.DelayCharge",
                          "value": "true"}],
                    "options": [{
                        "key": "Charger.EVC.Option.DelayChargeTime",
                        "valueType": "Integer",
                        "value": delayTime}
                    ]}
                ]}

        elif delayEnabled == "off":
            delayChargeRequest = {
                "chargePoints": [{
                    "connectorId": connectorID,
                    "programs": [{
                        "key": "Charger.EVC.Program.DelayCharge",
                        "value": "false"
                    }]
                }]
            }

        if delayChargeRequest:
            try:
                socket.send(json.dumps(delayChargeRequest).encode())
                print("Delay charge is successfully requested {}: {} minutes".format(delayEnabled, str(delayTime)))
                return {"command": self.command(), "result": "successful"}

            except Exception as e:
                print("Failed to send delay charge request: ", str(e))
                return {"command": self.command(), "result": "failed"}
        else:
            print('Second argument of delay-charge command is "on" or "off"')
            return {"command": self.command(), "result": "failed"}

import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    __options = ("-h", "-s", "-e", "-c", "--start", "--end", "--connector", "--help")
    __cmd = "eco-charge"
    __name = "Eco Charge"

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
        return """eco-charge [on/off] [options]: Eco-charge command, used with on/off arguments, start time and end times are given with option arguments
		OPTIONS:
			-h / --help: Show help
			-s / --start: Start time (In minutes)
			-e / --end: End time (In minutes)
			-c / --connector: Connector ID (default connector ID is 1)
		e.g
			eco-charge on -s 1320 -e 360 -c 1
		"""

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.__cmd, "result": "failed"}

        onOffArgument = argList.pop(0)
        startTime = 0
        endTime = 0
        connectorID = 1

        for i in range(len(argList)):
            if "-c" == argList[i] or "--connector" == argList[i]:
                if argList[i + 1]:
                    connectorID = int(argList[i + 1])
                    continue

            elif "-s" == argList[i] or "--start" == argList[i]:
                if argList[i + 1]:
                    startTime = int(argList[i + 1])
                    continue

            elif "-e" == argList[i] or "--end" == argList[i]:
                if argList[i + 1]:
                    endTime = int(argList[i + 1])
                    continue

        socket = kwargs.get('socket')
        print("Requesting echo charge: ", onOffArgument)

        try:
            if onOffArgument == "off":
                ecoChargeRequest = {"chargePoints": [{"connectorId": connectorID, "programs": [
                    {"key": "Charger.EVC.Program.EcoCharge", "value": "false"}]}]}
                socket.send(json.dumps(ecoChargeRequest).encode())
                return {"command": self.command(), "result": "successful"}

            elif onOffArgument == "on":
                ecoChargeRequest = {
                    "chargePoints": [{
                        "connectorId": connectorID,
                        "programs": [{
                            "key": "Charger.EVC.Program.EcoCharge",
                            "value": "true"
                        }],
                        "options": [
                            {
                                "key": "Charger.EVC.Option.EcoChargeStartTime",
                                "value": startTime
                            },
                            {
                                "key": "Charger.EVC.Option.EcoChargeStopTime",
                                "value": endTime
                            }]
                    }]
                }
                socket.send(json.dumps(ecoChargeRequest).encode())
                print("Eco charge is successfully requested {} with start time: {} end time: {}".format(onOffArgument,
                                                                                                        str(startTime),
                                                                                                        str(endTime)))
                return {"command": self.command(), "result": "successful"}

            else:
                raise Exception("Second argument should be on/off")

        except Exception as e:
            print("Failed to send eco-charge request: %s" % str(e))
            return {"command": self.command(), "result": "failed"}

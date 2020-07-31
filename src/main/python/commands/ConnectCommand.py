import datetime
import time
import json
import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "-p", "--port", "--help")
    cmd = "connect"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

    @staticmethod
    def info():
        return """connect [mac] [options]: Connect bluetooth command, second arg is mac address of target device
            OPTIONS:
                -p / --port : Specify target port  (Default port is 1)
                -h / --help : Show help
            e.g:
                connect CC:D3:C1:01:9A:78 --port 1
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.cmd, "result": "failed"}

        socket = kwargs.get('socket')
        print("Establishing connection..")

        macAddress = argList.pop(0)
        portNr = 1
        for i in range(len(argList)):
            if argList[i] == "-p" or argList[i] == "--port":
                portNr = argList[i + 1]

        try:
            socket.connect((macAddress, int(portNr)))
            print("Connection is established with {} over port number {}".format(str(macAddress), str(portNr)))

        except Exception as e:
            print("Failed connecting specified address %s - port %s - %s" % (macAddress, portNr, str(e)))
            return {"command": self.cmd, "result": "failed"}

        # Send time sync
        timeSyncRequest = {"MessageType": "TimeSync", "Timezone": "Europe/Istanbul",
                           "LocalTime": datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")}
        configParamRequest = {"MessageType": "ConfigurationParameterRequest"}

        socket.send(json.dumps(timeSyncRequest).encode())
        time.sleep(0.5)
        socket.send(json.dumps(configParamRequest).encode())

        return {"command": self.cmd, "result": "successful"}

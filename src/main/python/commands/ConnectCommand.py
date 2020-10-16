import datetime
import time
import json
import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-p", "--port")
    __cmd = "connect"
    __name = "Connect"
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
        return """connect [mac] [options]: Connect bluetooth command, second arg is mac address of target device
            OPTIONS:
                -p / --port : Specify target port  (Default port is 1)
            e.g:
                connect CC:D3:C1:01:9A:78 --port 1"""

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        socket = kwargs.get('socket')
        print("Establishing connection..")

        macAddress = argList.pop(0)
        portNr = 1
        name = kwargs.get('name', None)

        for i in range(len(argList)):
            if argList[i] == "-p" or argList[i] == "--port":
                portNr = argList[i + 1]

        try:
            socket.connect((macAddress, int(portNr)))
            print("Connection is established with {} over port number {}".format(str(macAddress), str(portNr)))

        except Exception as e:
            print("Failed connecting specified address %s - port %s - %s" % (macAddress, portNr, str(e)))
            return {"command": self.command(), "result": "failed"}

        # Send time sync
        timeSyncRequest = {"MessageType": "TimeSync", "Timezone": "Europe/Istanbul",
                           "LocalTime": datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")}
        configParamRequest = {"MessageType": "ConfigurationParameterRequest"}

        socket.send(json.dumps(timeSyncRequest).encode())
        time.sleep(0.5)
        socket.send(json.dumps(configParamRequest).encode())

        return {"command": self.command(), "result": "successful", "mac": macAddress, "portNumber": portNr, "name": name}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')
        print("Establishing connection..")

        macAddress = kwargs.get('mac')
        portNr = kwargs.get('port', 1)
        name = kwargs.get('name', None)

        try:
            socket.connect((macAddress, int(portNr)))
            print("Connection is established with {} over port number {}".format(str(macAddress), str(portNr)))

        except Exception as e:
            print("Failed connecting specified address %s - port %s - %s" % (macAddress, portNr, str(e)))
            return {"command": self.command(), "result": "failed"}

        # Send time sync
        timeSyncRequest = {"MessageType": "TimeSync", "Timezone": "Europe/Istanbul",
                           "LocalTime": datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")}
        configParamRequest = {"MessageType": "ConfigurationParameterRequest"}

        socket.send(json.dumps(timeSyncRequest).encode())
        time.sleep(0.5)
        socket.send(json.dumps(configParamRequest).encode())

        return {"command": self.command(), "result": "successful", "mac": macAddress, "portNumber": portNr, "name": name}

    def isDisplayed(self):
        return False

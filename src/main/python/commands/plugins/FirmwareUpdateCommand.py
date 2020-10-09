import json
import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    __options = ()
    __cmd = "firmware-update"
    __name = "Firmware Update"

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
        return """firmware-update [options]: Firmware update command, used to signal the start firmware update.
            OPTIONS:
                -
            e.g
                firmware-update
            """

    def execute(self, argList, **kwargs):
        socket = kwargs.get('socket')

        print("Requesting firmware update")

        firmwareUpdateRequest = {
            "chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.FirmwareUpdate"}]}]}

        try:
            socket.send(json.dumps(firmwareUpdateRequest).encode())

        except Exception as e:
            print("Failed to send firmware update request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Firmware update is successfully requested")
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')

        print("Requesting firmware update")

        firmwareUpdateRequest = {
            "chargePoints": [{"connectorId": 0, "command": [{"key": "Charger.EVC.Command.FirmwareUpdate"}]}]}

        try:
            socket.send(json.dumps(firmwareUpdateRequest).encode())

        except Exception as e:
            print("Failed to send firmware update request", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Firmware update is successfully requested")
        return {"command": self.command(), "result": "successful"}

    def setupUi(self):
        pass

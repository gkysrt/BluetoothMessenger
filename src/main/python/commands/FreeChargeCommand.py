import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "--help")
    cmd = "free-charge"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

    @staticmethod
    def info():
        return """free-charge [on/off] [options]: Free charging command, used to switch on/off free charge. Second arg is "on" or "off"
            OPTIONS:
                -h / --help : Show help
            e.g:
                free-charge on / free-charge off
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.cmd, "result": "failed"}

        # TODO: INCOMPLETE

        socket = kwargs.get('socket')

    # print("Requesting free charge")
    # socket.send(b'{"chargePoints": [{"connectorId": 1,"command": [{"key": "Charger.EVC.Command.Authorize"}]}]}')
    #
    # return {"command: free-charge"}

import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "--help")
    cmd = "disconnect"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

    @staticmethod
    def info():
        return """disconnect [options]: Disconnect command, disconnects from any existing connection
            OPTIONS:
                -h / --help : Show help
            e.g:
                disconnect
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.cmd, "result": "failed"}

        socket = kwargs.get('socket')
        print("Disconnecting..")

        try:
            socket.close()

        except Exception as e:
            print("Failed disconnecting: ", str(e))
            return {"command": self.cmd, "result": "failed"}

        # TODO: Should a disconnect request be sent to the machine?
        socket.close()
        print("Disconnected from peer")
        return {"command": self.cmd, "result": "successful"}

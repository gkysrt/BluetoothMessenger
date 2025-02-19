import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ()
    __cmd = "disconnect"
    __name = "Disconnect"
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
        return """disconnect [options]: Disconnect command, disconnects from any existing connection
            OPTIONS:
                -
            e.g:
                disconnect"""

    def execute(self, argList, **kwargs):
        socket = kwargs.get('socket')
        print("Disconnecting..")

        try:
            socket.close()

        except Exception as e:
            print("Failed disconnecting: ", str(e))
            return {"command": self.command(), "result": "failed"}

        # TODO: Should a disconnect request be sent to the machine?
        socket.close()
        print("Disconnected from peer")
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')
        print("Disconnecting..")

        try:
            socket.close()

        except Exception as e:
            print("Failed disconnecting: ", str(e))
            return {"command": self.command(), "result": "failed"}

        # TODO: Should a disconnect request be sent to the machine?
        socket.close()
        print("Disconnected from peer")
        return {"command": self.command(), "result": "successful"}

    def isDisplayed(self):
        return False

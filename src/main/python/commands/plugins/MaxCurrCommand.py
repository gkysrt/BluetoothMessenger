import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ()
    __cmd = "max-current"
    __name = "Max Current"

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
        return """max-current [amperes] [options]: Max current command, used to set max current value per phase.
            Second arg is max current value in amperes.
            OPTIONS:
                -
            """

    def execute(self, argList, **kwargs):
        # TODO: INCOMPLETE
        maxCurrent = int(argList.pop(0))

    def executeUI(self, **kwargs):
        # TODO: INCOMPLETE
        pass

    def setupUi(self):
        pass

import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    __options = ("-h", "--help")
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
                -h / --help : Show help
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        # TODO: INCOMPLETE
        maxCurrent = int(argList.pop(0))

    # for arg in argList:
    #     print()

import BaseCommand


class Command(BaseCommand.BaseCommand):
    def __init__(self):
        super().__init__()

    options = ("-h", "--help")
    cmd = "max-current"

    @classmethod
    def options(cls):
        return cls.options

    @classmethod
    def command(cls):
        return cls.cmd

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
            return {"command": self.cmd, "result": "failed"}

        # TODO: INCOMPLETE
        maxCurrent = int(argList.pop(0))

    # for arg in argList:
    #     print()

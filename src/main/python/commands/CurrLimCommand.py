import BaseCommand


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-h", "--help")
    __cmd = "limit-current"
    __name = "Limit Current"

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
        return """current-limit [amperes] [options]: Current limit command, second arg is limit value in amperes
            OPTIONS:
                -h / --help : Show help
            	-c / --connector: Specify a connector ID (default connector id is 1)
            e.g
                current-limit 20
            """

    def execute(self, argList, **kwargs):
        # TODO: INCOMPLETE
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        currentLimit = int(argList.pop(0))

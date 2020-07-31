import BaseCommand


class Command(BaseCommand.BaseCommand):
	def __init__(self):
		super().__init__()

	options = ("-h", "--help")
	cmd = "limit-current"

	@classmethod
	def options(cls):
		return cls.options

	@classmethod
	def command(cls):
		return cls.cmd

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
			return {"command": self.cmd, "result": "failed"}

		currentLimit = int(argList.pop(0))




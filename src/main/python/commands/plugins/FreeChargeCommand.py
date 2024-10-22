# import BaseCommand
#
#
# class Plugin(BaseCommand.BaseCommand):
#     def __init__(self, parent = None):
#         super().__init__(parent)
#
#     __options = ("-h", "--help")
#     __cmd = "free-charge"
#     __name = "Free Charge"
#
#     @classmethod
#     def options(cls):
#         return cls.__options
#
#     @classmethod
#     def command(cls):
#         return cls.__cmd
#
#     @classmethod
#     def name(cls):
#         return cls.__name
#
#     @staticmethod
#     def info():
#         return """free-charge [on/off] [options]: Free charging command, used to switch on/off free charge. Second arg is "on" or "off"
#             OPTIONS:
#                 -h / --help : Show help
#             e.g:
#                 free-charge on / free-charge off
#             """
#
#     def execute(self, argList, **kwargs):
#         if '-h' in argList or '--help' in argList:
#             print(self.info())
#             return {"command": self.command(), "result": "failed"}
#
#         # TODO: INCOMPLETE
#
#         socket = kwargs.get('socket')
#
#     def executeUI(self, **kwargs):
#         socket = kwargs.get('socket')
#
#     def setupUi(self):
#         pass
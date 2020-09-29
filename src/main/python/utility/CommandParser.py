import os
import importlib
import BaseCommand


class CommandParser(object):
    def __init__(self, name=None):
        super().__init__()

    # This method parses argument and executes related command with given kwargs
    def parse(self, argumentString, **kwargs):
        # If user typed in no specific command
        if argumentString == "help" or argumentString == "info":
            self.displayManual()
            return

        elif argumentString == "clear":
            os.system('clear')
            return

        elif argumentString == "":
            return

        argumentList = argumentString.split()

        # First argument is always the command, rest are the arguments, options etc.
        # Command is removed from argumentList
        commandString = argumentList.pop(0)

        if commandString in self.__cmdDict.keys():
            command = self.__cmdDict.get(commandString)
            return command.execute(argumentList, **kwargs)

        else:
            print("Command not recognized. Type \"help\" to display manual.")

    # Prints out all available commands' info
    def displayManual(self):
        for command in self.__cmdDict.values():
            print(command.info())

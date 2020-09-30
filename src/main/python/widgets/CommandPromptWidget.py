from PySide2 import QtWidgets, QtCore, QtGui
from widgets import CommandTextWidget
from utility import CommandParser


class CommandPromptWidget(QtWidgets.QWidget):
    terminalCommandRequested = QtCore.Signal(list, object)

    def __init__(self, model = None, parent=None):
        super().__init__(parent)
        self.__commandTextEdit = None
        self.__generalTextEdit = None
        self.__commandModel = model
        self.__commandParser = CommandParser.CommandParser()
        self.setupUi()
        self.initSignalsAndSlots()

    def setupUi(self):

        self.setStyleSheet("border: 1px solid rgb(80, 80, 80); background-color: rgb(64, 64, 64);"
                           "color: rgb(222, 222, 222); font-family: Ubuntu;")
        self.hide()
        self.setWindowFlag(QtCore.Qt.Window, True)
        self.setMinimumSize(640, 360)
        self.setProperty("commandPrompt", True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.__generalTextEdit = QtWidgets.QTextEdit(self)
        self.__generalTextEdit.setReadOnly(True)
        self.__generalTextEdit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.__commandTextEdit = CommandTextWidget.CommandTextWidget(self)

        layout.addWidget(self.__generalTextEdit)
        layout.addWidget(self.__commandTextEdit)

    def initSignalsAndSlots(self):
        self.__commandTextEdit.commandEntered.connect(self.onCommandEnter)

    def setCommandModel(self, model):
        self.__commandModel = model

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.setHidden(True)

        super().keyPressEvent(event)

    def onCommandEnter(self, text):
        self.printText(text)
        self.parse(text)

    # Prints text on terminal output window
    def printText(self, text, dateInfo = True):
        if dateInfo:
            dateString = QtCore.QDateTime.currentDateTime().toString('[hh:mm:ss] - : ')
        else:
            dateString = ""
        self.__generalTextEdit.insertPlainText("\n" + dateString + text + "\n")
        self.__generalTextEdit.moveCursor(QtGui.QTextCursor.End)

    # This method parses argument and executes related command with given kwargs
    def parse(self, argumentString, **kwargs):
        # If user typed in no specific command
        if argumentString == 'quit' or argumentString == 'exit' or argumentString == 'close':
            self.setHidden(True)
            return

        if argumentString == "help" or argumentString == "info":
            self.displayManual()
            return

        elif argumentString == "clear":
            self.__generalTextEdit.clear()
            return

        elif argumentString == "":
            return

        argumentList = argumentString.split()

        # First argument is always the command, rest are the arguments, options etc.
        # Command is removed from argumentList
        commandString = argumentList.pop(0)

        if commandString in self.__commandModel.getCommands():
            self.terminalCommandRequested.emit(argumentList, self.__commandModel.getCommand(commandString))

        else:
            self.printText("Command not recognized. Type \"help\" to display manual.", False)

    # Prints out all available commands' info
    def displayManual(self):
        commandObjects = [self.__commandModel.getCommand(key) for key in self.__commandModel.getCommands()]
        for command in commandObjects:
            self.printText(command.info(), False)


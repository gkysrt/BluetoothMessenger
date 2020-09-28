from PySide2 import QtWidgets, QtCore, QtGui
from widgets import CommandTextWidget


class CommandPromptWidget(QtWidgets.QWidget):
    def __init__(self, model = None, parent=None):
        super().__init__(parent)
        self.__commandTextEdit = None
        self.__generalTextEdit = None
        self.__model = model
        self.setupUi()
        self.initSignalsAndSlots()

    def setupUi(self):
        self.hide()
        self.setWindowFlag(QtCore.Qt.Window, True)
        self.setMinimumSize(480, 270)
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

    def setModel(self, model):
        self.__model = model

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.setHidden(True)

        super().keyPressEvent(event)

    def onCommandEnter(self, text):
        self.printText(text)

    # Prints text on terminal output window
    def printText(self, text):
        # TODO: Add date info to text here
        self.__generalTextEdit.insertPlainText(text + "\n")
        self.__generalTextEdit.moveCursor(QtGui.QTextCursor.End)

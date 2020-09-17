from PySide2 import QtWidgets, QtCore


class CommandPromptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.hide()
        self.setWindowFlag(QtCore.Qt.Window, True)
        self.setMinimumSize(480, 270)
        self.setProperty("commandPrompt", True)

    def initSignalsAndSlots(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.setHidden(True)

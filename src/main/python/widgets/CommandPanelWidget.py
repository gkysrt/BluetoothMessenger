from PySide2 import QtWidgets


class CommandPanelWidget(QtWidgets.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__tabWidget = None
        self.setupUi()
        self.initSignalsAndSlots()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText("Additional Commands")

        self.__tabWidget = QtWidgets.QTabWidget(self)
        self.__tabWidget.setMovable(False)

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.__tabWidget)

    def initSignalsAndSlots(self):
        pass

    def setIcon(self, icon):
        self.__iconLabel.setPixmap(icon)

    def setName(self, name):
        self.__nameLabel.setText("Device Name: %s".format(str(name)))

    def setMac(self, mac):
        self.__macLabel.setText("MAC Address: %s".format(str(mac)))

    def setStatus(self, status):
        # TODO: Should take enum and change status indicators and text accordingly
        self.__statusLabel.setText("Status: ..")

    def setDuration(self, time):
        # TODO: Duration calculation here
        self.__durationLabel.setText("Duration: %s".format(str(time)))

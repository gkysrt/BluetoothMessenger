from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from utility.PluginReader import PluginReader
from BaseCommand import BaseCommand
from commands.plugins import CurrLimCommand, DelayCommand, EcoCommand, FreeChargeCommand, InterfaceSettCommand, \
    InterfaceSettCommand, MaxCurrCommand, PowerOptCommand, ReconfigureCommand, ResetRfidCommand, AvailableCurrent, \
    CachedSessionCommand, FirmwareUpdateCommand, LockableCableCommand, PlugAndChargeCommand


class CommandPanelWidget(QtWidgets.QLabel):
    executeRequested = QtCore.Signal(object)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.__tabWidget = None
        self.__executeButton = None
        self.__commandModel = None

        self.setupUi()
        self.initSignalsAndSlots()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText("Additional Commands")

        self.__tabWidget = QtWidgets.QTabWidget(self)
        self.__tabWidget.setMovable(False)
        self.__tabWidget.tabBar().setUsesScrollButtons(True)

        self.__executeButton = QtWidgets.QPushButton(self)
        self.__executeButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.__executeButton.setText("Execute")

        self.constructTabs()

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.__tabWidget)
        mainLayout.addWidget(self.__executeButton)

    def constructTabs(self):
        if not self.__commandModel:
            return

        cmdDict = self.__commandModel.getCommandDict()
        self.__tabWidget.clear()

        for key in cmdDict:
            commandWidget = cmdDict.get(key)
            if commandWidget.isDisplayed():
                name = commandWidget.name()
                self.__tabWidget.addTab(commandWidget, name)

    def setCommandModel(self, model):
        self.__commandModel = model
        self.constructTabs()

    def initSignalsAndSlots(self):
        self.__executeButton.clicked.connect(lambda: self.executeRequested.emit(self.__tabWidget.currentWidget()))

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

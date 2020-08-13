from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets
from utility.PluginReader import PluginReader
from BaseCommand import BaseCommand
from commands import AuthorizeCommand, ConnectCommand, CurrLimCommand, DelayCommand, DisconnectCommand, EcoCommand, \
    FreeChargeCommand, InterfaceSettCommand, MaxCurrCommand, PauseCommand, PowerOptCommand, ReconfigureCommand, \
    ResetRfidCommand, ResumeCommand, ScanCommand, ServiceCommand, StartCommand, StopCommand


class CommandPanelWidget(QtWidgets.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__tabWidget = None
        self.__cmdDict = {}

        # Initialize commands, plug-ins
        self.initializeCommands()
        self.setupUi()
        self.initSignalsAndSlots()

    def initializeCommands(self):
        appCore = ApplicationCore.getInstance()
        externalCommandPluginsDict = {}
        if appCore.isFrozen():
            externalCommandPluginsDict = PluginReader.loadPlugins('plugins.commands', appCore.getPlugin('commands'))

        internalCommandPluginsDict = {}
        for subclass in BaseCommand.__subclasses__():
            internalCommandPluginsDict[subclass.command()] = subclass()

        internalCommandPluginsDict.update(externalCommandPluginsDict)
        print(internalCommandPluginsDict)

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

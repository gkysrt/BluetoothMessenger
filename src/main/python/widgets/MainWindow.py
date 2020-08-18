from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from delegates import ListViewDelegate
from widgets import ListHeaderWidget, ListView, DeviceWidget, CommandPanelWidget
from models import ModelFilter
from utility import QssLoader
from commands import AuthorizeCommand, PauseCommand, ResumeCommand, StartCommand, StopCommand, ScanCommand,\
	DisconnectCommand
import bluetooth


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__socket = None
		self.__scanButton = None
		self.__authorizeButton = None
		self.__startChargeButton = None
		self.__stopChargeButton = None
		self.__listView = None
		self.__listHeader = None
		self.__model = None
		self.__qssLoader = QssLoader.QssLoader()		# QssLoader instantiation
		self.setupUi()
		self.__authorizeCmd = None
		self.__pauseCmd = None
		self.__resumeCmd = None
		self.__startCmd = None
		self.__stopCmd = None
		self.__scanCmd = None
		self.__disconnectCmd = None
		self.initialize()
		self.initSignalsAndSlots()

	def setupUi(self):
		# Obtain app core
		appCore = ApplicationCore.getInstance()

		# Ask application core path of 'DefaultStyle.qss' and pass it to QssLoader's loadQss function
		# Set return value as style sheet of main window
		self.setStyleSheet(self.__qssLoader.loadQss(appCore.getQss('DefaultStyle.qss')))

		centralWidget = QtWidgets.QWidget(self)
		centralLayout = QtWidgets.QHBoxLayout(centralWidget)
		centralLayout.setSpacing(0)
		centralLayout.setContentsMargins(0, 0, 0, 0)
		self.setCentralWidget(centralWidget)

		# Construct left-side container widget
		listWindow = QtWidgets.QLabel(self)
		listWindow.setFixedWidth(250)
		listWindowLayout = QtWidgets.QVBoxLayout(listWindow)
		listWindowLayout.setContentsMargins(0, 0, 0, 0)
		listWindowLayout.setSpacing(0)

		# ListView that displays available devices and control  panel named listHeader
		self.__listView = ListView.ListView(listWindow)
		self.__listHeader = ListHeaderWidget.ListHeaderWidget(listWindow)

		# Initiate item delegate and set it as listView delegate
		listViewDelegate = ListViewDelegate.ListViewDelegate(self)
		self.__listView.setItemDelegate(listViewDelegate)

		listWindowLayout.addWidget(self.__listHeader)
		listWindowLayout.addWidget(self.__listView)

		# Construct right-side container widget
		deviceWindow = QtWidgets.QLabel(self)
		# deviceWindow.setStyleSheet("border: 1px solid rgb(64, 64, 64);")
		deviceWindowLayout = QtWidgets.QVBoxLayout(deviceWindow)
		deviceWindowLayout.setSpacing(0)
		deviceWindowLayout.setContentsMargins(0, 0, 0, 0)

		deviceWidget = DeviceWidget.DeviceWidget(deviceWindow)

		buttonContainerWidget = QtWidgets.QWidget(deviceWindow)
		buttonContainerLayout = QtWidgets.QHBoxLayout(buttonContainerWidget)
		buttonContainerLayout.setContentsMargins(8, 0, 8, 0)

		self.__authorizeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__authorizeButton.setText("Authorize")

		self.__startChargeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__startChargeButton.setText("Start")

		self.__stopChargeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__stopChargeButton.setText("Stop")

		buttonContainerLayout.addWidget(self.__authorizeButton)
		buttonContainerLayout.addWidget(self.__startChargeButton)
		buttonContainerLayout.addWidget(self.__stopChargeButton)

		commandPanelWidget = CommandPanelWidget.CommandPanelWidget(deviceWindow)

		deviceWindowLayout.addWidget(deviceWidget)
		deviceWindowLayout.addWidget(buttonContainerWidget)
		deviceWindowLayout.addWidget(commandPanelWidget)

		centralLayout.addWidget(listWindow)
		centralLayout.addWidget(deviceWindow)

	def initSignalsAndSlots(self):
		self.__authorizeButton.clicked.connect(self.onAuthorizeButtonClick)
		self.__startChargeButton.clicked.connect(self.onStartButtonClick)
		self.__stopChargeButton.clicked.connect(self.onStopButtonClick)
		self.__listHeader.scanSignal.connect(self.onScanSignal)
		self.__listHeader.disconnectSignal.connect(self.onDisconnectSignal)

	def initialize(self):
		self.initBluetoothSocket()
		self.__scanCmd = ScanCommand.Plugin()
		self.__disconnectCmd = DisconnectCommand.Plugin()
		self.__startCmd = StartCommand.Plugin()
		self.__authorizeCmd = AuthorizeCommand.Plugin()
		self.__pauseCmd = PauseCommand.Plugin()
		self.__resumeCmd = ResumeCommand.Plugin()
		self.__stopCmd = StopCommand.Plugin()
		self.__model = ModelFilter.ModelFilter(self)
		self.__listView.setModel(self.__model)

	def initBluetoothSocket(self):
		self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		super().keyPressEvent(event)

	def onStopButtonClick(self, checked = False):
		self.__stopCmd.execute()

	def onStartButtonClick(self, checked = False):
		self.__startCmd.execute()
		self.__pauseCmd.execute()
		self.__resumeCmd.execute()

	def onAuthorizeButtonClick(self, checked = False):
		self.__authorizeCmd.execute()

	def onScanSignal(self):
		returnDict = self.__scanCmd.executeUI()
		devices = returnDict.get("devices")
		self.__model.setDevices(devices)

	def onDisconnectSignal(self):
		print("disconnect")

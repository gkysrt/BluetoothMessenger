from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from delegates import ListViewDelegate
from widgets import ListHeaderWidget, ListView, DeviceWidget, CommandPanelWidget
from models import ModelFilter, ModelAdapter, Thread
from utility import QssLoader
from commands import AuthorizeCommand, PauseCommand, ResumeCommand, StartCommand, StopCommand, ScanCommand,\
	DisconnectCommand, ConnectCommand, ServiceCommand
import bluetooth


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__authorizeButton = None
		self.__startChargeButton = None
		self.__stopChargeButton = None

		self.__listView = None
		self.__listHeader = None

		self.__socket = None
		self.__model = None
		self.__modelAdapter = None

		self.__commandThread = None

		self.__authorizeCmd = None
		self.__pauseCmd = None
		self.__resumeCmd = None
		self.__startCmd = None
		self.__stopCmd = None
		self.__scanCmd = None
		self.__serviceCmd = None
		self.__connectCmd = None
		self.__disconnectCmd = None

		self.__qssLoader = QssLoader.QssLoader()		# QssLoader instantiation
		self.setupUi()
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
		self.__authorizeButton.setCursor(QtCore.Qt.PointingHandCursor)

		self.__startChargeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__startChargeButton.setText("Start")
		self.__startChargeButton.setCursor(QtCore.Qt.PointingHandCursor)

		self.__stopChargeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__stopChargeButton.setText("Stop")
		self.__stopChargeButton.setCursor(QtCore.Qt.PointingHandCursor)

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
		self.__commandThread.successful.connect(self.onCommandThreadSuccess)
		self.__authorizeButton.clicked.connect(self.onAuthorizeButtonClick)
		self.__startChargeButton.clicked.connect(self.onStartButtonClick)
		self.__stopChargeButton.clicked.connect(self.onStopButtonClick)
		self.__listHeader.scanSignal.connect(self.onScanSignal)
		self.__listHeader.disconnectSignal.connect(self.onDisconnectSignal)
		self.__listView.clicked.connect(self.onListItemClick)

	def initialize(self):
		self.initBluetoothSocket()
		self.__commandThread = Thread.Thread(self)

		self.__scanCmd = ScanCommand.Plugin()
		self.__serviceCmd = ServiceCommand.Plugin()
		self.__connectCmd = ConnectCommand.Plugin()
		self.__disconnectCmd = DisconnectCommand.Plugin()
		self.__startCmd = StartCommand.Plugin()
		self.__authorizeCmd = AuthorizeCommand.Plugin()
		self.__pauseCmd = PauseCommand.Plugin()
		self.__resumeCmd = ResumeCommand.Plugin()
		self.__stopCmd = StopCommand.Plugin()

		self.__modelAdapter = ModelAdapter.ModelAdapter()
		self.__model = ModelFilter.ModelFilter(adapter=self.__modelAdapter, parent = self)
		self.__listView.setModel(self.__model)

	def initBluetoothSocket(self):
		self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	# ------------- EVENT HANDLING -------------
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		super().keyPressEvent(event)

	# ------------- SLOTS -------------
	def onStopButtonClick(self, checked = False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__stopCmd.executeUI, socket=self.__socket)

	def onStartButtonClick(self, checked = False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__startCmd.executeUI, socket = self.__socket)
			self.__commandThread.start(self.__pauseCmd.executeUI, socket=self.__socket)
			self.__commandThread.start(self.__resumeCmd.executeUI, socket=self.__socket)

	def onAuthorizeButtonClick(self, checked = False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__authorizeCmd.executeUI, socket = self.__socket)

	def onScanSignal(self):
		if not self.__commandThread.isRunning():
			self.__listHeader.setScanButtonEnabled(False)
			self.__commandThread.start(self.__scanCmd.executeUI)

	def onDisconnectSignal(self):
		if self.__model.connectedDevice() is not None and not self.__commandThread.isRunning():
			self.__commandThread.start(self.__disconnectCmd.executeUI, socket = self.__socket)

	def onCommandThreadSuccess(self, returnValue):
		if returnValue.get('command') == 'scan':
			devices = returnValue.get('devices')
			newDevices = []
			for device in devices:
				mac, name, uuid = device
				services = bluetooth.find_service(address=mac)
				newDevices.append((mac, name, uuid, services))

			self.__model.setDevices(devices)
			self.__listHeader.setScanButtonEnabled(True)

	def onCommandThreadFail(self, exception):
		print("Command thread failed to execute command - Error: {}".format(str(exception)))

	def onListItemClick(self, index):
		if not self.__commandThread.isRunning():
			device = self.__model.dataFromIndex(index)
			self.__commandThread.start(self.__connectCmd.executeUI, socket = self.__socket, name = device.name(), mac = device.mac(), port = 1)

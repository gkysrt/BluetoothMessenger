from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from delegates import ListViewDelegate
from models.Enum import EVCStatus
from widgets import ListHeaderWidget, ListView, DeviceWidget, CommandPanelWidget
from models import ModelFilter, ModelAdapter, Thread
from utility import QssLoader
from commands import AuthorizeCommand, PauseCommand, ResumeCommand, StartCommand, StopCommand, ScanCommand,\
	DisconnectCommand, ConnectCommand, ServiceCommand
import bluetooth
import ResponseReceiver
import DeviceContext
import json


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		# Initializing variables that'll be used in MainWindow class

		# Buttons
		self.__authorizeButton = None
		self.__startChargeButton = None
		self.__stopChargeButton = None

		# Widgets
		self.__listView = None
		self.__listHeader = None
		self.__deviceWidget = None
		self.__commandPanelWidget = None

		# Response receiver & device context that's affected by received messages
		self.__responseReceiver = None
		self.__deviceContext = None

		# BT socket, ListModel and adapter for the model
		self.__socket = None
		self.__model = None
		self.__modelAdapter = None

		# Threads for executing commands & loading services of scanned BT devices
		self.__commandThread = None
		self.__serviceLoaderThread = None

		# Some main commands
		self.__authorizeCmd = None
		self.__pauseCmd = None
		self.__resumeCmd = None
		self.__startCmd = None
		self.__stopCmd = None
		self.__scanCmd = None
		self.__serviceCmd = None
		self.__connectCmd = None
		self.__disconnectCmd = None

		# QSSLoader class, used to load qss
		self.__qssLoader = QssLoader.QssLoader()		# QssLoader instantiation

		# Setup UI and widgets
		self.setupUi()

		# Initialize objects and start program
		self.initialize()

		# Initialize signals and slots
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

		self.__deviceWidget = DeviceWidget.DeviceWidget(deviceWindow)

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

		self.__commandPanelWidget = CommandPanelWidget.CommandPanelWidget(deviceWindow)
		# self.__commandPanelWidget.setFixedHeight(200)

		deviceWindowLayout.addWidget(self.__deviceWidget)
		deviceWindowLayout.addWidget(buttonContainerWidget)
		deviceWindowLayout.addWidget(self.__commandPanelWidget)

		centralLayout.addWidget(listWindow)
		centralLayout.addWidget(deviceWindow)

	def initSignalsAndSlots(self):
		self.__commandThread.successful.connect(self.onCommandThreadSuccess)
		self.__commandThread.failed.connect(self.onCommandThreadFail)
		self.__commandPanelWidget.executeRequested.connect(self.onExecuteRequest)
		self.__authorizeButton.clicked.connect(self.onAuthorizeButtonClick)
		self.__startChargeButton.clicked.connect(self.onStartButtonClick)
		self.__stopChargeButton.clicked.connect(self.onStopButtonClick)
		self.__listHeader.scanSignal.connect(self.onScanSignal)
		self.__listHeader.disconnectSignal.connect(self.onDisconnectSignal)
		self.__listView.clicked.connect(self.onListItemClick)
		self.__model.rowsInserted.connect(self.onDeviceAdded)
		self.__model.modelReset.connect(self.onDeviceModelReset)
		self.__responseReceiver.responseReceived.connect(self.onResponseReceived)

	def initialize(self):
		self.initBluetoothSocket()

		self.__responseReceiver = ResponseReceiver.ResponseReceiver()
		self.__deviceContext = DeviceContext.DeviceContext()

		self.__commandThread = Thread.Thread(self)
		self.__serviceLoaderThread = Thread.Thread(self)

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
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.AUTHORIZATION.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.CHARGE_POINT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.FIRMWARE_UPDATE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.CHARGE_SESSION.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.CURRENT_CHARGE_SESSION.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.CACHED_CHARGE_SESSION.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.DELAY_CHARGE_REMAINING_TIME.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.MASTER_CARD.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.USER_CARD.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.METRICS.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.MIN_CURRENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.MAX_CURRENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.POWER_OPT_MAX.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCStatus.POWER_OPT_MIN.value)

	def initBluetoothSocket(self):
		self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.__socket.setblocking(True)

	def loadServices(self, **kwargs):
		firstRow = kwargs.get('first')
		lastRow = kwargs.get('last')
		for i in range(firstRow, lastRow):
			index = self.__model.index(i, 0)
			device = self.__model.dataFromIndex(index)
			services = bluetooth.find_service(address=device.mac())
			self.__model.setData(index, ('services', services), QtCore.Qt.EditRole)

		print("Services are loaded for scanned devices")

	# ------------- EVENT HANDLING -------------
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

		if event.key() == QtCore.Qt.Key_S:
			self.onScanSignal()

		if event.key() == QtCore.Qt.Key_D:
			self.onDisconnectSignal()

		super().keyPressEvent(event)

	def closeEvent(self, event):
		if self.__responseReceiver.isRunning():
			self.__responseReceiver.stop()
			self.__responseReceiver.close()

		self.__commandThread.quit()
		self.__serviceLoaderThread.quit()
		super().closeEvent(event)

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

	def onExecuteRequest(self, commandObject):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(commandObject.executeUI, socket=self.__socket, connectors=self.__deviceContext.chargePoints(), connector = self.__deviceWidget.selectedConnector())

	def onCommandThreadSuccess(self, returnValue):
		if not returnValue:
			return

		if returnValue.get('command') == 'scan':
			self.__listHeader.setScanButtonEnabled(True)

			if returnValue.get('result') == 'successful':
				devices = returnValue.get('devices')
				self.__model.setDevices(devices)

		if returnValue.get('command') == 'connect':
			if returnValue.get('result') == 'failed':
				self.initBluetoothSocket()
			elif returnValue.get('result') == 'successful':
				connectedDeviceName = returnValue.get('name', None)
				connectedDeviceMac = returnValue.get('mac', None)
				matchingDevices = self.__model.getFilteredDevices(name=connectedDeviceName, mac=connectedDeviceMac)
				connectedDevice = None
				if len(matchingDevices) == 1:
					connectedDevice = matchingDevices.pop()

				if connectedDevice:
					index = self.__model.indexFromData(connectedDevice)
					self.__model.setData(index, ('isConnected', True), QtCore.Qt.EditRole)

				self.__responseReceiver.setSocket(self.__socket.dup())
				if not self.__responseReceiver.isRunning():
					self.__deviceContext.reset()
					self.__responseReceiver.start()
			self.__listView.repaint()

		if returnValue.get('command') == 'disconnect' and returnValue.get('result') == 'successful':
			disconnectedDeviceIndex = self.__model.indexFromData(self.__model.connectedDevice())
			self.__model.setData(disconnectedDeviceIndex, ('isConnected', False), QtCore.Qt.EditRole)

			self.initBluetoothSocket()
			if self.__responseReceiver.isRunning():
				self.__responseReceiver.stop()
				self.__deviceContext.reset()

			self.__listView.repaint()

		print(returnValue)

	def onCommandThreadFail(self, exception):
		print("Command thread failed to execute command - Error: {}".format(str(exception)))

	def onListItemClick(self, index):
		if not self.__commandThread.isRunning():
			device = self.__model.dataFromIndex(index)
			if not device.isConnected():
				self.__commandThread.start(self.__connectCmd.executeUI, socket = self.__socket, name = device.name(), mac = device.mac(), port = 1)

	def onDeviceAdded(self, parent, first, last):
		self.__serviceLoaderThread.start(self.loadServices, first=first, last=last)

	def onDeviceModelReset(self):
		self.__serviceLoaderThread.start(self.loadServices, first=0, last=self.__model.rowCount(QtCore.QModelIndex()))

	def onResponseReceived(self, response):
		# Handling the response from device
		# TODO: An adapter that transforms incoming messages from device?
		jsonResponse = json.loads(response)
		chargePoints = jsonResponse.get('chargePoints')
		for chargePoint in chargePoints:
			connectorID = chargePoint.get('connectorId')
			self.__deviceContext.addChargePoint(connectorID)

			statuses = chargePoint.get('status', [])
			for status in statuses:
				self.__deviceContext.setState(status.get('value'), status.get('key'), connectorID)

			settings = chargePoint.get('settings', [])
			for setting in settings:
				self.__deviceContext.setState(setting.get('value'), setting.get('key'), connectorID)

			programs = chargePoint.get('programs', [])
			for program in programs:
				self.__deviceContext.setState(program.get('value'), program.get('key'), connectorID)

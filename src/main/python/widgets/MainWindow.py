from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from delegates import ListViewDelegate
from models.Enum import EVCStatus, EVCProgram, EVCSetting, EVCError, EVCOptions
from widgets import ListHeaderWidget, ListView, DeviceWidget, CommandPanelWidget, CommandPromptWidget
from models import ModelFilter, ModelAdapter, Thread, CommandModel
from utility import QssLoader, PluginReader
from commands import AuthorizeCommand, PauseCommand, ResumeCommand, StartCommand, StopCommand, ScanCommand, \
	DisconnectCommand, ConnectCommand, ServiceCommand
import bluetooth
import ResponseReceiver
import DeviceContext
import json
from BaseCommand import BaseCommand
from commands.plugins import CurrLimCommand, DelayCommand, EcoCommand, FreeChargeCommand, InterfaceSettCommand, \
	InterfaceSettCommand, MaxCurrCommand, PowerOptCommand, ReconfigureCommand, ResetRfidCommand, AvailableCurrent, \
	CachedSessionCommand, FirmwareUpdateCommand, LockableCableCommand, PlugAndChargeCommand


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
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
		self.__commandPromptWidget = None

		# Response receiver & device context that's affected by received messages
		self.__responseReceiver = None
		self.__deviceContext = None

		# BT socket, ListModel and adapter for the model
		self.__socket = None
		self.__model = None
		self.__modelAdapter = None
		self.__commandModel = None

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
		self.__qssLoader = QssLoader.QssLoader()  # QssLoader instantiation

		# Setup UI and widgets
		self.setupUi()

		# Initialize objects and start program
		self.initialize()

		# Initialize all commands and fill CommandModel
		self.initializeCommands()

		# Initialize signals and slots
		self.initSignalsAndSlots()

		self.setFocus()

	def setupUi(self):
		# Obtain app core
		appCore = ApplicationCore.getInstance()

		# Ask application core path of 'DefaultStyle.qss' and pass it to QssLoader's loadQss function
		# Set return value as style sheet of main window
		self.setStyleSheet(self.__qssLoader.loadQss(appCore.getQss('DefaultStyle.qss')))

		self.__commandPromptWidget = CommandPromptWidget.CommandPromptWidget(parent=self)

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
		# deviceWindowLayout.setContentsMargins(8, 8, 8, 8)

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

		deviceWindowLayout.addWidget(self.__deviceWidget)
		deviceWindowLayout.addWidget(buttonContainerWidget)
		deviceWindowLayout.addWidget(self.__commandPanelWidget)

		centralLayout.addWidget(listWindow)
		centralLayout.addWidget(deviceWindow)

	def initSignalsAndSlots(self):
		# Whenever a command executed inside commandThread,
		# it'll result in running onCommandThreadSuccess() or onCommandThreadFail() functions
		self.__commandThread.successful.connect(self.onCommandThreadSuccess)
		self.__commandThread.failed.connect(self.onCommandThreadFail)

		# Commands are executed through CommandPanel's Execute button, Authorize - Start - Stop buttons and CommandPrompt
		# They're all tied to their respective methods, all will be run inside CommandThread
		self.__commandPanelWidget.executeRequested.connect(self.onExecuteRequest)
		self.__commandPromptWidget.terminalCommandRequested.connect(self.onTerminalCommandRequest)
		self.__authorizeButton.clicked.connect(self.onAuthorizeButtonClick)
		self.__startChargeButton.clicked.connect(self.onStartButtonClick)
		self.__stopChargeButton.clicked.connect(self.onStopButtonClick)

		# ListHeader's button click signals are connected to their respective methods
		self.__listHeader.scanSignal.connect(self.onScanSignal)
		self.__listHeader.disconnectSignal.connect(self.onDisconnectSignal)
		self.__listHeader.commandPromptSignal.connect(self.onCommandPromptSignal)

		# ListView's item click signal is connected to onListItemClick() method.
		self.__listView.clicked.connect(self.onListItemClick)

		# Model's item inserted and model reset signals, connected to their respective functions
		self.__model.rowsInserted.connect(self.onDeviceAdded)
		self.__model.modelReset.connect(self.onDeviceModelReset)

		# Whenever a response is received from ResponseReceiver class, onResponseReceived() method runs
		self.__responseReceiver.responseReceived.connect(self.onResponseReceived)

		# DeviceContext is an observable that holds various info on connected device.
		# Whenever a new chargePoint info received deviceContext's signals will run their respective methods
		self.__deviceContext.chargePointAdded.emit(self.onConnectorAddedContext)
		self.__deviceContext.chargePointRemoved.emit(self.onConnectorRemovedContext)

	def initialize(self):
		# Start off by initializing bluetooth socket
		self.initBluetoothSocket()

		# Initialize ResponseReceiver and DeviceContext for possible connections
		self.__responseReceiver = ResponseReceiver.ResponseReceiver()
		self.__deviceContext = DeviceContext.DeviceContext()

		# Ready CommandThread and ServiceLoader thread
		self.__commandThread = Thread.Thread(self)
		self.__serviceLoaderThread = Thread.Thread(self)

		# Initialize ModelAdapter and hand it over to the device model
		self.__modelAdapter = ModelAdapter.ModelAdapter()
		self.__model = ModelFilter.ModelFilter(adapter=self.__modelAdapter, parent=self)

		# Set ListView's model
		self.__listView.setModel(self.__model)

		# Initialize CommandModel that'll inhabit all scanned available commands
		self.__commandModel = CommandModel.CommandModel(self)

		# Add deviceWidget object as an observer of some attributes of self.__deviceWidget
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

		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.TIMEZONE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.LOCKABLE_CABLE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.AVAILABLE_CURRENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.POWER_OPTIMIZER.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.PLUG_AND_CHARGE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.ETHERNET.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCSetting.CELLULAR.value)

		self.__deviceContext.attach(self.__deviceWidget, EVCProgram.ECO_CHARGE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCProgram.DELAY_CHARGE.value)

		self.__deviceContext.attach(self.__deviceWidget, EVCError.CONTRACTOR_WELDED.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.CONTRACTOR_RESPONSE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.INTERLOCK_LOCK.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.INTERLOCK_UNLOCK.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.PP.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.CP_DIODE.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_VOLTAGE_P1.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_VOLTAGE_P2.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_VOLTAGE_P3.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.UNDER_VOLTAGE_P1.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.UNDER_VOLTAGE_P2.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.UNDER_VOLTAGE_P3.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_CURRENT_P1.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_CURRENT_P2.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OVER_CURRENT_P3.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.RESIDUAL_CURRENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.PROTECTIVE_EARTH.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.RFID.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.INTERLOCK_PERMANENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.OCP_PERMANENT.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.LOAD_BALANCE_MODULE_1.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.LOAD_BALANCE_MODULE_2.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.LOAD_BALANCE_MODULE_3.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCError.HMI_EXTERNAL.value)

		self.__deviceContext.attach(self.__deviceWidget, EVCOptions.DELAY_CHARGE_TIME.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCOptions.ECO_CHARGE_START_TIME.value)
		self.__deviceContext.attach(self.__deviceWidget, EVCOptions.ECO_CHARGE_STOP_TIME.value)

	# This method aims to initialize both external and internal commands
	def initializeCommands(self):
		appCore = ApplicationCore.getInstance()
		externalCommandPluginsDict = {}
		if appCore.isFrozen():
			externalCommandPluginsDict = PluginReader.loadPlugins('plugins.commands', appCore.getPlugin('commands'),
																  BaseCommand)

		internalCommandPluginsDict = {}
		for subclass in BaseCommand.__subclasses__():
			# Check if internal command plugin is inside commands.plugin package
			if subclass.__module__.startswith('commands.plugin'):
				internalCommandPluginsDict[subclass.command()] = subclass()

		internalCommandPluginsDict.update(externalCommandPluginsDict)
		self.__commandModel.setCommands(internalCommandPluginsDict)

		self.__scanCmd = ScanCommand.Plugin()
		self.__serviceCmd = ServiceCommand.Plugin()
		self.__connectCmd = ConnectCommand.Plugin()
		self.__disconnectCmd = DisconnectCommand.Plugin()
		self.__startCmd = StartCommand.Plugin()
		self.__authorizeCmd = AuthorizeCommand.Plugin()
		self.__pauseCmd = PauseCommand.Plugin()
		self.__resumeCmd = ResumeCommand.Plugin()
		self.__stopCmd = StopCommand.Plugin()

		# self.__commandModel.addCommand(self.__disconnectCmd)

		self.__commandPanelWidget.setCommandModel(self.__commandModel)
		self.__commandPromptWidget.setCommandModel(self.__commandModel)

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

		if event.key() == QtCore.Qt.Key_T:
			self.onCommandPromptSignal()
		super().keyPressEvent(event)

	def resizeEvent(self, event):
		self.__deviceWidget.setFixedHeight(event.size().height() / 5 * 2)
		self.__commandPanelWidget.setFixedHeight(event.size().height() / 2)
		super().resizeEvent(event)

	def closeEvent(self, event):
		if self.__responseReceiver.isRunning():
			self.__responseReceiver.stop()
			self.__responseReceiver.close()

		self.__commandThread.quit()
		self.__serviceLoaderThread.quit()
		super().closeEvent(event)

	# ------------- SLOTS -------------
	def onStopButtonClick(self, checked=False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__stopCmd.executeUI, socket=self.__socket)

	def onStartButtonClick(self, checked=False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__startCmd.executeUI, socket=self.__socket)
			self.__commandThread.start(self.__pauseCmd.executeUI, socket=self.__socket)
			self.__commandThread.start(self.__resumeCmd.executeUI, socket=self.__socket)

	def onAuthorizeButtonClick(self, checked=False):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(self.__authorizeCmd.executeUI, socket=self.__socket)

	def onScanSignal(self):
		if not self.__commandThread.isRunning():
			self.__listHeader.setScanButtonEnabled(False)
			self.__commandThread.start(self.__scanCmd.executeUI)

	def onDisconnectSignal(self):
		if self.__model.connectedDevice() is not None and not self.__commandThread.isRunning():
			self.__commandThread.start(self.__disconnectCmd.executeUI, socket=self.__socket)

	def onCommandPromptSignal(self):
		self.__commandPromptWidget.show()

	def onExecuteRequest(self, commandObject):
		if not self.__commandThread.isRunning():
			self.__commandThread.start(commandObject.executeUI,
									   socket=self.__socket,
									   connectors=self.__deviceContext.chargePoints(),
									   connector=self.__deviceWidget.selectedConnector())

	def onTerminalCommandRequest(self, argList, commandObject):
		self.__commandThread.start(commandObject.execute,
								   argList=argList,
								   socket=self.__socket,
								   connectors=self.__deviceContext.chargePoints(),
								   connector=self.__deviceWidget.selectedConnector())

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
					# Update model's connected device
					self.__model.setData(index, ('isConnected', True), QtCore.Qt.EditRole)
					# Set deviceWidget attributes with connected device attributes
					self.__deviceWidget.setName(connectedDevice.name())
					self.__deviceWidget.setMac(connectedDevice.mac())
					self.__deviceWidget.setDuration(0)

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

			if self.__model.connectedDevice():
				self.__commandThread.start(self.__disconnectCmd.executeUI, socket=self.__socket)

			if not device.isConnected():
				self.__commandThread.start(self.__connectCmd.executeUI, socket=self.__socket, name=device.name(),
										   mac=device.mac(), port=1)

	def onDeviceAdded(self, parent, first, last):
		self.__serviceLoaderThread.start(self.loadServices, first=first, last=last)

	def onDeviceModelReset(self):
		self.__serviceLoaderThread.start(self.loadServices, first=0, last=self.__model.rowCount(QtCore.QModelIndex()))

	def onConnectorAddedContext(self, connector):
		print("SIGNALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		self.__deviceWidget.addConnector(connector)

	def onConnectorRemovedContext(self, connector):
		self.__deviceWidget.removeConnector(connector)

	def onResponseReceived(self, response):
		# Handling the response from device
		# TODO: An adapter that transforms incoming messages from device?
		jsonResponse = json.loads(response)
		chargePoints = jsonResponse.get('chargePoints', [])
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

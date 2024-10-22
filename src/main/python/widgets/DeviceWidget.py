from PySide2 import QtWidgets, QtCore
from observer import BaseObserver
from models.Enum import EVCStatus, EVCError, EVCProgram, EVCSetting
import ApplicationCore


class DeviceWidget(QtWidgets.QLabel, BaseObserver.BaseObserver):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__iconLabel = None
		self.__nameLabel = None
		self.__macLabel = None
		self.__statusLabel = None
		self.__durationLabel = None
		self.__connectorComboBox = None
		self.__authorizationStatusLabel = None
		self.__ecoChargeLabel = None
		self.__delayChargeLabel = None
		self.__errorLabel = None
		self.__internetConnectionLabel = None

		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		headerWidth = 110

		appContext = ApplicationCore.ApplicationCore.getInstance()

		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setMaximumHeight(220)
		# self.setStyleSheet("border: 1px solid rgb(155, 155, 155);")
		mainLayout = QtWidgets.QHBoxLayout(self)

		self.__iconLabel = QtWidgets.QLabel(self)
		self.__iconLabel.setAlignment(QtCore.Qt.AlignCenter)
		# self.__iconLabel.setText("ICON HERE")
		# self.__iconLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")
		self.__iconLabel.setPixmap(appContext.getIcon("evc_device.png"))
		self.__iconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

		detailWidget = QtWidgets.QWidget(self)
		detailLayout = QtWidgets.QVBoxLayout(detailWidget)
		detailLayout.setContentsMargins(0, 0, 0, 0)
		detailLayout.setSpacing(0)

		nameContainerWidget = QtWidgets.QWidget(detailWidget)
		nameContainerLayout = QtWidgets.QHBoxLayout(nameContainerWidget)
		nameContainerLayout.setContentsMargins(0, 0, 0, 0)
		nameHeaderLabel = QtWidgets.QLabel("Device Name", nameContainerWidget)
		nameHeaderLabel.setStyleSheet("font: bold;")
		nameHeaderLabel.setFixedWidth(headerWidth)
		self.__nameLabel = QtWidgets.QLabel(nameContainerWidget)
		nameContainerLayout.addWidget(nameHeaderLabel)
		nameContainerLayout.addWidget(self.__nameLabel)

		macContainerWidget = QtWidgets.QWidget(detailWidget)
		macContainerLayout = QtWidgets.QHBoxLayout(macContainerWidget)
		macContainerLayout.setContentsMargins(0, 0, 0, 0)
		macHeaderLabel = QtWidgets.QLabel("Mac Address")
		macHeaderLabel.setStyleSheet("font: bold;")
		macHeaderLabel.setFixedWidth(headerWidth)
		self.__macLabel = QtWidgets.QLabel(macContainerWidget)
		macContainerLayout.addWidget(macHeaderLabel)
		macContainerLayout.addWidget(self.__macLabel)

		authorizationStatusContainerWidget = QtWidgets.QWidget(detailWidget)
		authorizationStatusContainerLayout = QtWidgets.QHBoxLayout(authorizationStatusContainerWidget)
		authorizationStatusContainerLayout.setContentsMargins(0, 0, 0, 0)
		authorizationStatusHeaderLabel = QtWidgets.QLabel("Auth. Status")
		authorizationStatusHeaderLabel.setStyleSheet("font: bold;")
		authorizationStatusHeaderLabel.setFixedWidth(headerWidth)
		authorizationStatusHeaderLabel.setToolTip("Authentication Status")
		self.__authorizationStatusLabel = QtWidgets.QLabel(authorizationStatusContainerWidget)
		authorizationStatusContainerLayout.addWidget(authorizationStatusHeaderLabel)
		authorizationStatusContainerLayout.addWidget(self.__authorizationStatusLabel)

		statusContainerWidget = QtWidgets.QWidget(detailWidget)
		statusContainerLayout = QtWidgets.QHBoxLayout(statusContainerWidget)
		statusContainerLayout.setContentsMargins(0, 0, 0, 0)
		statusHeaderLabel = QtWidgets.QLabel("CP Status")
		statusHeaderLabel.setStyleSheet("font: bold;")
		statusHeaderLabel.setFixedWidth(headerWidth)
		statusHeaderLabel.setToolTip("Charge Point Status")
		self.__statusLabel = QtWidgets.QLabel(statusContainerWidget)
		statusContainerLayout.addWidget(statusHeaderLabel)
		statusContainerLayout.addWidget(self.__statusLabel)

		durationContainerWidget = QtWidgets.QWidget(detailWidget)
		durationContainerLayout = QtWidgets.QHBoxLayout(durationContainerWidget)
		durationContainerLayout.setContentsMargins(0, 0, 0, 0)
		durationHeaderLabel = QtWidgets.QLabel("Duration")
		durationHeaderLabel.setStyleSheet("font: bold;")
		durationHeaderLabel.setFixedWidth(headerWidth)
		self.__durationLabel = QtWidgets.QLabel(durationContainerWidget)
		durationContainerLayout.addWidget(durationHeaderLabel)
		durationContainerLayout.addWidget(self.__durationLabel)

		detailLayout.addWidget(nameContainerWidget)
		detailLayout.addWidget(macContainerWidget)
		detailLayout.addWidget(authorizationStatusContainerWidget)
		detailLayout.addWidget(statusContainerWidget)
		detailLayout.addWidget(durationContainerWidget)

		detailWidget2 = QtWidgets.QWidget(self)
		detailLayout2 = QtWidgets.QVBoxLayout(detailWidget2)
		detailLayout2.setContentsMargins(0, 0, 0, 0)
		detailLayout2.setSpacing(0)

		connectorContainerWidget = QtWidgets.QWidget(detailWidget2)
		connectorContainerLayout = QtWidgets.QHBoxLayout(connectorContainerWidget)
		connectorText = QtWidgets.QLabel(connectorContainerWidget)
		connectorText.setText("Connectors")
		connectorText.setStyleSheet("font: bold;")
		connectorText.setFixedWidth(headerWidth)
		self.__connectorComboBox = QtWidgets.QComboBox(connectorContainerWidget)
		self.__connectorComboBox.setCursor(QtCore.Qt.PointingHandCursor)
		# self.__connectorComboBox.addItem("1")
		# self.__connectorComboBox.addItem("2")
		connectorContainerLayout.addWidget(connectorText)
		connectorContainerLayout.addWidget(self.__connectorComboBox)

		ecoChargeContainerWidget = QtWidgets.QWidget(detailWidget2)
		ecoChargeContainerLayout = QtWidgets.QHBoxLayout(ecoChargeContainerWidget)
		ecoChargeText = QtWidgets.QLabel(ecoChargeContainerWidget)
		ecoChargeText.setText("Eco Charge")
		ecoChargeText.setStyleSheet("font: bold;")
		ecoChargeText.setFixedWidth(headerWidth)
		self.__ecoChargeLabel = QtWidgets.QLabel(ecoChargeContainerWidget)
		ecoChargeContainerLayout.addWidget(ecoChargeText)
		ecoChargeContainerLayout.addWidget(self.__ecoChargeLabel)

		delayChargeContainerWidget = QtWidgets.QWidget(detailWidget2)
		delayChargeContainerLayout = QtWidgets.QHBoxLayout(delayChargeContainerWidget)
		delayChargeText = QtWidgets.QLabel(delayChargeContainerWidget)
		delayChargeText.setText("Delay Charge")
		delayChargeText.setStyleSheet("font: bold;")
		delayChargeText.setFixedWidth(headerWidth)
		self.__delayChargeLabel = QtWidgets.QLabel(delayChargeContainerWidget)
		delayChargeContainerLayout.addWidget(delayChargeText)
		delayChargeContainerLayout.addWidget(self.__delayChargeLabel)

		errorContainerWidget = QtWidgets.QWidget(detailWidget2)
		errorContainerLayout = QtWidgets.QHBoxLayout(errorContainerWidget)
		errorText = QtWidgets.QLabel(delayChargeContainerWidget)
		errorText.setText("Error")
		errorText.setStyleSheet("font: bold;")
		errorText.setFixedWidth(headerWidth)
		self.__errorLabel = QtWidgets.QLabel(errorContainerWidget)
		errorContainerLayout.addWidget(errorText)
		errorContainerLayout.addWidget(self.__errorLabel)

		internetConnectionContainerWidget = QtWidgets.QWidget(detailWidget2)
		internetConnectionContainerLayout = QtWidgets.QHBoxLayout(internetConnectionContainerWidget)
		internetConnectionText = QtWidgets.QLabel(internetConnectionContainerWidget)
		internetConnectionText.setText("Internet Conn.")
		internetConnectionText.setStyleSheet("font: bold;")
		internetConnectionText.setFixedWidth(headerWidth)
		self.__internetConnectionLabel = QtWidgets.QLabel(internetConnectionContainerWidget)
		internetConnectionContainerLayout.addWidget(internetConnectionText)
		internetConnectionContainerLayout.addWidget(self.__internetConnectionLabel)

		detailLayout2.addWidget(connectorContainerWidget)
		detailLayout2.addWidget(ecoChargeContainerWidget)
		detailLayout2.addWidget(delayChargeContainerWidget)
		detailLayout2.addWidget(errorContainerWidget)
		detailLayout2.addWidget(internetConnectionContainerWidget)

		mainLayout.addWidget(self.__iconLabel)
		mainLayout.addWidget(detailWidget)
		mainLayout.addWidget(detailWidget2)

		self.__durationLabel.setText(None)
		self.setMac(None)
		self.setName(None)
		self.setCPStatus(None)
		self.setAuthStatus(None)
		self.setEcoChargeStatus(None)
		self.setDelayChargeStatus(None)
		self.setErrorStatus(None)
		self.setInternetConnectionStatus("-")

	def initSignalsAndSlots(self):
		pass

	def setIcon(self, icon):
		self.__iconLabel.setPixmap(icon)

	def setName(self, name):
		if name is None:
			text = "-"
		else:
			text = name
		self.__nameLabel.setText("{}".format(str(text)))

	def setMac(self, mac):
		if mac is None:
			text = "-"
		else:
			text = mac
		self.__macLabel.setText("{}".format(str(text)))

	def setCPStatus(self, status):
		# TODO: Should take enum and change status indicators and text accordingly
		if status is None:
			text = "-"
		else:
			text = str(status).replace(EVCStatus.CHARGE_POINT.value + ".", "")
		self.__statusLabel.setText("{}".format(text))

	def setAuthStatus(self, status):
		# TODO: Should take enum and change status indicators and text accordingly
		text = status
		if status is None:
			text = "-"
		else:
			text = status
		self.__authorizationStatusLabel.setText("{}".format(str(text)))

	def setEcoChargeStatus(self, status):
		if status:
			text = "Enabled"
		elif status is None:
			text = "-"
		else:
			text = "Disabled"

		self.__ecoChargeLabel.setText(text)

	def setDelayChargeStatus(self, status):
		if status:
			text = "Enabled"
		elif status is None:
			text = "-"
		else:
			text = "Disabled"

		self.__delayChargeLabel.setText(text)

	def setErrorStatus(self, status):
		if status is None:
			text = "-"
		else:
			text = status
		self.__errorLabel.setText(str(text))

	def setInternetConnectionStatus(self, status):
		if status is None:
			text = "-"
		else:
			text = status
		self.__internetConnectionLabel.setText(str(text))

	def setDuration(self, time):
		# Incoming time is in minutes
		if time is None:
			self.__durationLabel.setText("-")
			return

		day = int(time / (60 * 24))
		hour = int(time / 60) % 24
		minute = time % 60

		if day > 0:
			durationString = "{} days - {} hours - {} minutes".format(str(day), str(hour), str(minute))
		elif hour > 0:
			durationString = "{} hours - {} minutes".format(str(hour), str(minute))
		else:
			durationString = "{} minutes".format(str(minute))

		self.__durationLabel.setText(durationString)

	# Sets connectors of connector combobox
	def setConnectors(self, connectors):
		for connector in connectors:
			self.__connectorComboBox.addItem(str(connector))

	# Adds a connector to connector combobox
	def addConnector(self, connector):
		print("connector eklendi bee", connector)
		self.__connectorComboBox.addItem(str(connector))

	def removeConnector(self, connector):
		pass

	def resizeEvent(self, event):
		self.__iconLabel.setMaximumWidth(self.__iconLabel.height())
		self.__iconLabel.setMinimumWidth(self.width() / 8)
		super().resizeEvent(event)

	# DeviceWidget class is an observer. This class receives related updates from DeviceContext class
	def update(self, **kwargs):
		print("DeviceWidget received info on evc state: {}".format(str(kwargs)))
		connectorID = kwargs.get('connectorID')
		key = kwargs.get('key')
		value = kwargs.get('value', None)

		if key == EVCStatus.AUTHORIZATION.value:
			self.setAuthStatus(value)

		elif key == EVCStatus.CHARGE_POINT.value:
			self.setCPStatus(value)

		elif key == EVCStatus.FIRMWARE_UPDATE.value:
			pass

		elif key == EVCStatus.CHARGE_SESSION.value:
			pass

		elif key == EVCStatus.CURRENT_CHARGE_SESSION.value:
			self.setDuration(value.get('duration'))

		elif key == EVCStatus.CACHED_CHARGE_SESSION.value:
			pass

		elif key == EVCStatus.DELAY_CHARGE_REMAINING_TIME.value:
			pass

		elif key == EVCStatus.MASTER_CARD.value:
			pass

		elif key == EVCStatus.USER_CARD.value:
			pass

		elif key == EVCStatus.METRICS.value:
			pass

		elif key == EVCStatus.MIN_CURRENT.value:
			pass

		elif key == EVCStatus.MAX_CURRENT.value:
			pass

		elif key == EVCStatus.POWER_OPT_MIN.value:
			pass

		elif key == EVCStatus.POWER_OPT_MAX.value:
			pass

		elif key == EVCProgram.ECO_CHARGE.value:
			print("eco charge", value)
			self.setEcoChargeStatus(value)

		elif key == EVCProgram.DELAY_CHARGE.value:
			print("delcharge", value)

			self.setDelayChargeStatus(value)

		elif key == EVCSetting.TIMEZONE.value:
			pass

		elif key == EVCSetting.LOCKABLE_CABLE.value:
			pass

		elif key == EVCSetting.AVAILABLE_CURRENT.value:
			pass

		elif key == EVCSetting.POWER_OPTIMIZER.value:
			pass

		elif key == EVCSetting.PLUG_AND_CHARGE.value:
			pass

		elif key == EVCSetting.ETHERNET.value:
			pass

		elif key == EVCSetting.CELLULAR.value:
			pass

	def selectedConnector(self):
		connectorNo = None
		connectorText = self.__connectorComboBox.currentText()
		if connectorText:
			connectorNo = int(connectorText)
		return connectorNo

from PySide2 import QtWidgets, QtCore
from observer import BaseObserver
from models.Enum import EVCStatus
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

		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		headerWidth = 110

		appContext = ApplicationCore.ApplicationCore.getInstance()

		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setMaximumHeight(200)
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
		self.__authorizationStatusLabel = QtWidgets.QLabel(authorizationStatusContainerWidget)
		authorizationStatusContainerLayout.addWidget(authorizationStatusHeaderLabel)
		authorizationStatusContainerLayout.addWidget(self.__authorizationStatusLabel)

		statusContainerWidget = QtWidgets.QWidget(detailWidget)
		statusContainerLayout = QtWidgets.QHBoxLayout(statusContainerWidget)
		statusContainerLayout.setContentsMargins(0, 0, 0, 0)
		statusHeaderLabel = QtWidgets.QLabel("Device Status")
		statusHeaderLabel.setStyleSheet("font: bold;")
		statusHeaderLabel.setFixedWidth(headerWidth)
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

		self.__durationLabel.setText("-")
		self.setMac("-")
		self.setName("-")
		self.setDeviceStatus("-")
		self.setAuthStatus("-")

		detailLayout.addWidget(nameContainerWidget)
		detailLayout.addWidget(macContainerWidget)
		detailLayout.addWidget(authorizationStatusContainerWidget)
		detailLayout.addWidget(statusContainerWidget)
		detailLayout.addWidget(durationContainerWidget)

		detailWidget2 = QtWidgets.QWidget(self)
		detailLayout2 = QtWidgets.QVBoxLayout(detailWidget2)
		detailLayout2.setContentsMargins(0, 0, 0, 0)

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

		# TODO: To be deleted
		spacer = QtWidgets.QWidget(detailWidget2)
		spacer.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

		detailLayout2.addWidget(connectorContainerWidget)
		detailLayout2.addWidget(spacer)

		mainLayout.addWidget(self.__iconLabel)
		mainLayout.addWidget(detailWidget)
		mainLayout.addWidget(detailWidget2)

	def initSignalsAndSlots(self):
		pass

	def setIcon(self, icon):
		self.__iconLabel.setPixmap(icon)

	def setName(self, name):
		self.__nameLabel.setText("{}".format(str(name)))

	def setMac(self, mac):
		self.__macLabel.setText("{}".format(str(mac)))

	def setDeviceStatus(self, status):
		# TODO: Should take enum and change status indicators and text accordingly
		self.__statusLabel.setText("{}".format(str(status)))

	def setAuthStatus(self, status):
		# TODO: Should take enum and change status indicators and text accordingly
		self.__authorizationStatusLabel.setText("{}".format(str(status)))

	def setDuration(self, time):
		# TODO: Duration calculation here
		# Incoming time is in minutes
		day = int(time / (60 * 24))
		hour = int(time / 60)
		minute = time % 60

		if day > 0:
			durationString = "{} days - {} hours - {} minutes".format(str(day), str(hour), str(minute))
		elif hour > 0:
			durationString = "{} hours - {} minutes".format(str(hour), str(minute))
		else:
			durationString = "{} minutes".format(str(minute))

		self.__durationLabel.setText(durationString)

	def setChargePoints(self, chargePoints):
		for chargePoint in chargePoints:
			self.__connectorComboBox.addItem(str(chargePoint))

	def resizeEvent(self, event):
		self.__iconLabel.setMaximumWidth(self.__iconLabel.height())
		super().resizeEvent(event)

	def update(self, **kwargs):
		print("DeviceWidget received info on evc state: {}".format(str(kwargs)))
		connectorID = kwargs.get('connectorID')
		key = kwargs.get('key')
		value = kwargs.get('value')

		if key == EVCStatus.AUTHORIZATION.value:
			pass

		elif key == EVCStatus.CHARGE_POINT.value:
			pass

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

	def selectedConnector(self):
		return int(self.__connectorComboBox.currentText())

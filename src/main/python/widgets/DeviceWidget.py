from PySide2 import QtWidgets, QtCore
from observer import BaseObserver
import json
from models.Enum import EVCStatus


class DeviceWidget(QtWidgets.QLabel, BaseObserver.BaseObserver):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__iconLabel = None
		self.__nameLabel = None
		self.__macLabel = None
		self.__statusLabel = None
		self.__durationLabel = None

		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		headerWidth = 110

		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setMaximumHeight(200)
		mainLayout = QtWidgets.QHBoxLayout(self)
		self.__iconLabel = QtWidgets.QLabel(self)
		self.__iconLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.__iconLabel.setText("ICON HERE")
		self.__iconLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		detailWidget = QtWidgets.QWidget(self)
		detailLayout = QtWidgets.QVBoxLayout(detailWidget)
		detailLayout.setContentsMargins(0, 0, 0, 0)

		nameContainerWidget = QtWidgets.QWidget(detailWidget)
		nameContainerLayout = QtWidgets.QHBoxLayout(nameContainerWidget)
		nameHeaderLabel = QtWidgets.QLabel("Device Name", nameContainerWidget)
		nameHeaderLabel.setStyleSheet("font: bold;")
		nameHeaderLabel.setFixedWidth(headerWidth)
		self.__nameLabel = QtWidgets.QLabel(nameContainerWidget)
		nameContainerLayout.addWidget(nameHeaderLabel)
		nameContainerLayout.addWidget(self.__nameLabel)

		macContainerWidget = QtWidgets.QWidget(detailWidget)
		macContainerLayout = QtWidgets.QHBoxLayout(macContainerWidget)
		macHeaderLabel = QtWidgets.QLabel("Mac Address")
		macHeaderLabel.setStyleSheet("font: bold;")
		macHeaderLabel.setFixedWidth(headerWidth)
		self.__macLabel = QtWidgets.QLabel(macContainerWidget)
		macContainerLayout.addWidget(macHeaderLabel)
		macContainerLayout.addWidget(self.__macLabel)

		statusContainerWidget = QtWidgets.QWidget(detailWidget)
		statusContainerLayout = QtWidgets.QHBoxLayout(statusContainerWidget)
		statusHeaderLabel = QtWidgets.QLabel("Device Status")
		statusHeaderLabel.setStyleSheet("font: bold;")
		statusHeaderLabel.setFixedWidth(headerWidth)
		self.__statusLabel = QtWidgets.QLabel(statusContainerWidget)
		statusContainerLayout.addWidget(statusHeaderLabel)
		statusContainerLayout.addWidget(self.__statusLabel)

		durationContainerWidget = QtWidgets.QWidget(detailWidget)
		durationContainerLayout = QtWidgets.QHBoxLayout(durationContainerWidget)
		durationHeaderLabel = QtWidgets.QLabel("Duration")
		durationHeaderLabel.setStyleSheet("font: bold;")
		durationHeaderLabel.setFixedWidth(headerWidth)
		self.__durationLabel = QtWidgets.QLabel(durationContainerWidget)
		durationContainerLayout.addWidget(durationHeaderLabel)
		durationContainerLayout.addWidget(self.__durationLabel)

		self.__durationLabel.setText("-")
		self.setMac("CC:3F:48:FD:4D:77")
		self.setName("am337x-evmsk")
		self.setStatus("Ready")

		detailLayout.addWidget(nameContainerWidget)
		detailLayout.addWidget(macContainerWidget)
		detailLayout.addWidget(statusContainerWidget)
		detailLayout.addWidget(durationContainerWidget)

		mainLayout.addWidget(self.__iconLabel)
		mainLayout.addWidget(detailWidget)


	def initSignalsAndSlots(self):
		pass

	def setIcon(self, icon):
		self.__iconLabel.setPixmap(icon)

	def setName(self, name):
		self.__nameLabel.setText("{}".format(str(name)))

	def setMac(self, mac):
		self.__macLabel.setText("{}".format(str(mac)))

	def setStatus(self, status):
		# TODO: Should take enum and change status indicators and text accordingly
		self.__statusLabel.setText("{}".format(str(status)))

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

	def resizeEvent(self, event):
		self.__iconLabel.setMaximumWidth(self.__iconLabel.height())
		super().resizeEvent(event)

	def update(self, **kwargs):
		print("DeviceWidget received info on evc state: {}".format(str(kwargs)))
		connectorID = kwargs.get('connectorID')
		key = kwargs.get('key')
		value = kwargs.get('value')
		if key == EVCStatus.CURRENT_CHARGE_SESSION.value:
			self.setDuration(value.get('duration'))
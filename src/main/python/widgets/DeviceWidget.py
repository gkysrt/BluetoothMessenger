from PySide2 import QtWidgets


class DeviceWidget(QtWidgets.QLabel):
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
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setMaximumHeight(200)
		mainLayout = QtWidgets.QHBoxLayout(self)
		self.__iconLabel = QtWidgets.QLabel(self)
		self.__iconLabel.setText("ICON HERE")
		self.__iconLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		detailWidget = QtWidgets.QWidget(self)
		detailLayout = QtWidgets.QVBoxLayout(detailWidget)
		detailLayout.setContentsMargins(0, 0, 0, 0)

		self.__nameLabel = QtWidgets.QLabel(detailWidget)
		self.__nameLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		self.__macLabel = QtWidgets.QLabel(detailWidget)
		self.__macLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		self.__statusLabel = QtWidgets.QLabel(detailWidget)
		self.__statusLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		self.__durationLabel = QtWidgets.QLabel(detailWidget)
		self.__durationLabel.setStyleSheet("border: 1px solid rgb(64, 64, 64);")

		# bottomSpacerWidget = QtWidgets.QWidget(detailWidget)
		# bottomSpacerWidget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

		self.setDuration("")
		self.setMac("")
		self.setName("")
		self.setStatus("")

		detailLayout.addWidget(self.__nameLabel)
		detailLayout.addWidget(self.__macLabel)
		detailLayout.addWidget(self.__statusLabel)
		detailLayout.addWidget(self.__durationLabel)
		# detailLayout.addWidget(bottomSpacerWidget)

		mainLayout.addWidget(self.__iconLabel)
		mainLayout.addWidget(detailWidget)

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

	def resizeEvent(self, event):
		self.__iconLabel.setMaximumWidth(self.__iconLabel.height())
		super().resizeEvent(event)

from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtGui, QtCore


class ListHeaderWidget(QtWidgets.QLabel):
	scanSignal = QtCore.Signal()
	disconnectSignal = QtCore.Signal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.__scanButton = None
		self.__disconnectButton = None
		self.__commandPromptButton = None
		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		self.setFixedHeight(48)
		layout = QtWidgets.QHBoxLayout(self)
		layout.setContentsMargins(8, 0, 8, 0)
		layout.setSpacing(8)

		appCore = ApplicationCore.getInstance()

		self.__scanButton = QtWidgets.QPushButton(self)
		self.__scanButton.setIcon(QtGui.QPixmap(appCore.getIcon('bluetooth_scan.png')))
		self.__scanButton.setFixedSize(40, 40)
		self.__scanButton.setProperty('listHeader', True)
		self.__scanButton.setIconSize(QtCore.QSize(30, 30))
		self.__scanButton.setToolTip("Scan")

		self.__disconnectButton = QtWidgets.QPushButton(self)
		self.__disconnectButton.setIcon(QtGui.QIcon(appCore.getIcon('bluetooth_disabled.png')))
		self.__disconnectButton.setFixedSize(40, 40)
		self.__disconnectButton.setProperty('listHeader', True)
		self.__disconnectButton.setIconSize(QtCore.QSize(30, 30))
		self.__disconnectButton.setToolTip("Disconnect")

		rightSpacerWidget = QtWidgets.QWidget(self)
		rightSpacerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		layout.addWidget(self.__scanButton)
		layout.addWidget(self.__disconnectButton)
		layout.addWidget(rightSpacerWidget)

	def initSignalsAndSlots(self):
		self.__scanButton.clicked.connect(self.scanSignal.emit)
		self.__disconnectButton.clicked.connect(self.disconnectSignal.emit)

	def setScanButtonEnabled(self, enabled):
		self.__scanButton.setEnabled(bool(enabled))

	def setDisconnectButtonEnabled(self, enabled):
		self.__disconnectButton.setEnabled(bool(enabled))
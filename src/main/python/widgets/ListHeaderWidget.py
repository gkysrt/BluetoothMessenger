from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtGui, QtCore


class ListHeaderWidget(QtWidgets.QLabel):
	scanSignal = QtCore.Signal()
	disconnectSignal = QtCore.Signal()
	commandPromptSignal = QtCore.Signal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.__scanButton = None
		self.__disconnectButton = None
		self.__commandPromptButton = None
		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		self.setStyleSheet("QLabel{background-color: rgb(181, 181, 181);"
						   "border-bottom-right-radius: 3px;"
						   "border-bottom: 1px solid rgb(155, 155, 155); "
						   "border-right: 1px solid rgb(155, 155, 155);}")
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
		self.__scanButton.setCursor(QtCore.Qt.PointingHandCursor)

		self.__disconnectButton = QtWidgets.QPushButton(self)
		self.__disconnectButton.setIcon(QtGui.QIcon(appCore.getIcon('bluetooth_disabled.png')))
		self.__disconnectButton.setFixedSize(40, 40)
		self.__disconnectButton.setProperty('listHeader', True)
		self.__disconnectButton.setIconSize(QtCore.QSize(30, 30))
		self.__disconnectButton.setToolTip("Disconnect")
		self.__disconnectButton.setCursor(QtCore.Qt.PointingHandCursor)

		self.__commandPromptButton = QtWidgets.QPushButton(self)
		self.__commandPromptButton.setIcon(QtGui.QIcon(appCore.getIcon('terminal_icon_32.png')))
		self.__commandPromptButton.setFixedSize(40, 40)
		self.__commandPromptButton.setProperty('listHeader', True)
		self.__commandPromptButton.setIconSize(QtCore.QSize(24, 24))
		self.__commandPromptButton.setToolTip("Command Prompt")
		self.__commandPromptButton.setCursor(QtCore.Qt.PointingHandCursor)

		rightSpacerWidget = QtWidgets.QWidget(self)
		rightSpacerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		layout.addWidget(self.__scanButton)
		layout.addWidget(self.__disconnectButton)
		layout.addWidget(rightSpacerWidget)
		layout.addWidget(self.__commandPromptButton)

	def initSignalsAndSlots(self):
		self.__scanButton.clicked.connect(self.scanSignal.emit)
		self.__disconnectButton.clicked.connect(self.disconnectSignal.emit)
		self.__commandPromptButton.clicked.connect(self.commandPromptSignal.emit)

	def setScanButtonEnabled(self, enabled):
		self.__scanButton.setEnabled(bool(enabled))

	def setDisconnectButtonEnabled(self, enabled):
		self.__disconnectButton.setEnabled(bool(enabled))

	def setCommandPromptButtonEnabled(self, enabled):
		self.__commandPromptButton.setEnabled(bool(enabled))

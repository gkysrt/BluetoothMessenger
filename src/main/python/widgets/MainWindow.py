from ApplicationCore import ApplicationCore
from PySide2 import QtWidgets, QtCore
from widgets import ListHeaderWidget, ListView, DeviceWidget
from models import ModelFilter
from utility import QssLoader


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__authorizeButton = None
		self.__startChargeButton = None
		self.__stopChargeButton = None
		self.__listView = None
		self.__listHeader = None
		self.__model = None
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

		listWindowLayout.addWidget(self.__listHeader)
		listWindowLayout.addWidget(self.__listView)

		# Construct right-side container widget
		deviceWindow = QtWidgets.QLabel(self)
		deviceWindowLayout = QtWidgets.QVBoxLayout(deviceWindow)

		deviceWidget = DeviceWidget.DeviceWidget(deviceWindow)

		buttonContainerWidget = QtWidgets.QWidget(deviceWindow)
		buttonContainerLayout = QtWidgets.QHBoxLayout(buttonContainerWidget)

		self.__authorizeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__startChargeButton = QtWidgets.QPushButton(buttonContainerWidget)
		self.__stopChargeButton = QtWidgets.QPushButton(buttonContainerWidget)

		buttonContainerLayout.addWidget(self.__authorizeButton)
		buttonContainerLayout.addWidget(self.__startChargeButton)
		buttonContainerLayout.addWidget(self.__stopChargeButton)

		deviceWindowLayout.addWidget(deviceWidget)
		deviceWindowLayout.addWidget(buttonContainerWidget)

		centralLayout.addWidget(listWindow)
		centralLayout.addWidget(deviceWindow)

	def initSignalsAndSlots(self):
		pass

	def initialize(self):
		self.__model = ModelFilter.ModelFilter(self)
		self.__listView.setModel(self.__model)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

		super().keyPressEvent(event)

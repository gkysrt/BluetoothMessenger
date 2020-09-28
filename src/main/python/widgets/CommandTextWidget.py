from PySide2 import QtWidgets, QtCore, QtGui
import ApplicationCore
from utility import DataStructures


class CommandTextWidget(QtWidgets.QLineEdit):
	commandEntered = QtCore.Signal(str)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.__commandStack = DataStructures.Stack()
		self.__commandStack.setLimit(50)

		self.__enterAction = None

		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		self.setClearButtonEnabled(False)

		appContext = ApplicationCore.ApplicationCore.getInstance()
		enterIcon = QtGui.QIcon(appContext.getIcon('enter_16.png'))
		self.__enterAction = self.addAction(enterIcon, QtWidgets.QLineEdit.TrailingPosition)

	def initSignalsAndSlots(self):
		self.returnPressed.connect(self.onReturnPress)
		self.__enterAction.triggered.connect(self.onReturnPress)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Up:
			text = self.__commandStack.softPop()
			if text:
				self.setText(text)

		elif event.key() == QtCore.Qt.Key_Down:
			text = self.__commandStack.reverseSoftPop()
			# We do not check text integrity here because we want to give blank space to user in case of an extensive
			# Down arrow key press
			self.setText(text)

		super().keyPressEvent(event)

	def onReturnPress(self):
		returnedText = self.text()
		if self.text():
			self.__commandStack.append(returnedText)
			self.commandEntered.emit(returnedText)
		self.clear()

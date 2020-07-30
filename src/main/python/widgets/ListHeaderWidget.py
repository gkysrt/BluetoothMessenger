from PySide2 import QtWidgets


class ListHeaderWidget(QtWidgets.QLabel):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi()
		self.initSignalsAndSlots()

	def setupUi(self):
		self.setStyleSheet("QWidget{border: 1px solid red;}")
		self.setFixedHeight(48)
		layout = QtWidgets.QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(4)

	def initSignalsAndSlots(self):
		pass

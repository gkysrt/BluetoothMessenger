from PySide2 import QtWidgets


class ListView(QtWidgets.QListView):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.initSignalsAndSlots()
		self.setStyleSheet("border:1px solid blue;")

	def initSignalsAndSlots(self):
		pass

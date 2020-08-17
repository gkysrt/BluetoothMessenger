from PySide2 import QtWidgets, QtCore


class ListView(QtWidgets.QListView):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.initSignalsAndSlots()
		self.setMouseTracking(True)
		# self.setCursor(QtCore.Qt.PointingHandCursor)

	def initSignalsAndSlots(self):
		pass

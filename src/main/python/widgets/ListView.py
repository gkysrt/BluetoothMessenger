from PySide2 import QtWidgets, QtCore


class ListView(QtWidgets.QListView):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.initSignalsAndSlots()
		self.setMouseTracking(True)

	def initSignalsAndSlots(self):
		pass

	def mouseMoveEvent(self, event):
		if self.indexAt(event.pos()).isValid():
			self.setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.setCursor(QtCore.Qt.ArrowCursor)
		super().mouseMoveEvent(event)

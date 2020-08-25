from PySide2 import QtWidgets, QtCore


class ListView(QtWidgets.QListView):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.initSignalsAndSlots()
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.setMouseTracking(True)

	def initSignalsAndSlots(self):
		self.customContextMenuRequested.connect(self.onContextMenuRequest)

	def mouseMoveEvent(self, event):
		if self.indexAt(event.pos()).isValid():
			self.setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.setCursor(QtCore.Qt.ArrowCursor)
		super().mouseMoveEvent(event)

	def onContextMenuRequest(self, pos):
		clickIndex = self.indexAt(pos)
		if clickIndex.isValid():
			device = self.model().dataFromIndex(clickIndex)
			print(device)
			print(device.services())
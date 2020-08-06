from PySide2 import QtWidgets, QtCore, QtGui
from models.Enum import DeviceTypes


class ListViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__evenColor = QtGui.QColor(64, 64, 64)
		self.__oddColor = QtGui.QColor(80, 80, 80)

	def paint(self, painter, option, index):
		painter.save()
		row = index.row()
		device = index.data(QtCore.Qt.UserRole)
		rectangle = option.rect

		deviceName = device.name()
		deviceMac = device.mac()
		isDeviceConnected = device.isConnected()
		deviceType = device.deviceType()
		deviceStatus = None
		if deviceType == DeviceTypes.EVC:
			deviceStatus = device.status()

		isEvenNr = True if (row % 2) == 0 else False

		painter.fillRect(rectangle, self.__evenColor) if isEvenNr else painter.fillRect(rectangle, self.__oddColor)

		painter.restore()
		super().paint(painter, option, index)

	def sizeHint(self, option, index):
		return QtCore.QSize(option.rect.width(), 80)

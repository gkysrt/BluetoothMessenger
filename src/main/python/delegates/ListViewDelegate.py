from PySide2 import QtWidgets, QtCore, QtGui
from models.Enum import DeviceTypes


class ListViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__nameRect = QtCore.QRect()
		self.__evenColor = QtGui.QColor(64, 64, 64)
		self.__oddColor = QtGui.QColor(80, 80, 80)
		self.__textColor = QtGui.QColor(200, 200, 200)
		self.__topLeftMargin = QtCore.QPoint(5, 5)

	def paint(self, painter, option, index):
		super().paint(painter, option, index)
		painter.save()
		row = index.row()
		device = index.data(QtCore.Qt.UserRole)
		rectangle = option.rect
		fontMetrics = option.fontMetrics
		painter.setPen(self.__textColor)

		deviceName = device.name()
		deviceMac = device.mac()
		isDeviceConnected = device.isConnected()
		deviceType = device.deviceType()
		deviceStatus = None
		if deviceType == DeviceTypes.EVC:
			deviceStatus = device.status()

		isEvenNr = True if (row % 2) == 0 else False
		painter.fillRect(rectangle, self.__evenColor) if isEvenNr else painter.fillRect(rectangle, self.__oddColor)

		iconRect = QtCore.QRect(option.rect.topLeft() + self.__topLeftMargin, QtCore.QPoint(option.rect.width() - 10, option.rect.y() + option.rect.height() / 2))
		nameRect = QtCore.QRect(option.rect.topLeft() + self.__topLeftMargin, QtCore.QPoint(option.rect.width() - 10, option.rect.y() + option.rect.height() / 2))
		print(option.rect)
		print(nameRect)

		painter.drawText(nameRect, 0, fontMetrics.elidedText(deviceName, QtCore.Qt.ElideRight, nameRect.width()))
		painter.restore()

	def sizeHint(self, option, index):
		return QtCore.QSize(option.rect.width(), 60)
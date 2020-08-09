from PySide2 import QtWidgets, QtCore, QtGui
from models.Enum import DeviceTypes


class ListViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__nameRect = QtCore.QRect()

		self.__topMargin = 5
		self.__bottomMargin = 5
		self.__leftMargin = 5
		self.__rightMargin = 5
		self.__spacing = 5

		self.__topLeftMarginPoint = QtCore.QPoint(self.__leftMargin, self.__topMargin)

		self.__evenColor = QtGui.QColor(64, 64, 64)
		self.__oddColor = QtGui.QColor(80, 80, 80)
		self.__textColor = QtGui.QColor(200, 200, 200)

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

		iconRect = QtCore.QRect(option.rect.topLeft() + self.__topLeftMarginPoint, QtCore.QPoint(option.rect.height() - self.__bottomMargin - self.__topMargin, option.rect.y() + option.rect.height() - self.__bottomMargin))
		nameRect = QtCore.QRect(QtCore.QPoint(iconRect.topRight().x() + self.__spacing, iconRect.topRight().y()), QtCore.QPoint(option.rect.width() - self.__rightMargin, option.rect.y() + option.rect.height() / 2))
		macRect = QtCore.QRect()
		connectionRect = QtCore.QRect()

		print(option.rect)
		print(nameRect)

		painter.drawText(nameRect, 0, fontMetrics.elidedText(deviceName, QtCore.Qt.ElideRight, nameRect.width()))

		painter.drawText(iconRect, 0, "icon\nhere")
		painter.drawRect(iconRect)

		painter.restore()

	def sizeHint(self, option, index):
		return QtCore.QSize(option.rect.width(), 60)

	def setContentMargins(self, left, top, right, bottom):
		self.__leftMargin = int(left)
		self.__topMargin = int(top)
		self.__rightMargin = int(right)
		self.__bottomMargin = int(bottom)

	def contentMargins(self):
		return self.__leftMargin, self.__topMargin, self.__rightMargin, self.__bottomMargin

	def setSpacing(self, spacing):
		self.__spacing = int(spacing)

	def spacing(self):
		return self.__spacing

	def setPrimaryBackgroundColor(self, color):
		self.__evenColor = color

	def setSecondaryBackgroundColor(self, color):
		self.__oddColor = color

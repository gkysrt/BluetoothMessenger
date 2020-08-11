from PySide2 import QtWidgets, QtCore, QtGui
from models.Enum import DeviceTypes
from ApplicationCore import ApplicationCore


class ListViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.__nameRect = QtCore.QRect()

		self.__topMargin = 5
		self.__bottomMargin = 5
		self.__leftMargin = 5
		self.__rightMargin = 5
		self.__spacing = 5

		self.__oddColor = QtGui.QColor(166, 166, 166)
		self.__evenColor = QtGui.QColor(191, 191, 191)
		self.__textColor = QtGui.QColor(64, 64, 64)

		appCore = ApplicationCore.getInstance()
		self.__iconEVC = QtGui.QPixmap(appCore.getIcon('evc_device.png'))
		self.__iconUndefined = QtGui.QPixmap(appCore.getIcon('bluetooth.png'))
		self.__iconPhone = QtGui.QPixmap(appCore.getIcon('phone_device.png'))
		self.__iconHeadphones = QtGui.QPixmap()
		self.__iconLaptop = QtGui.QPixmap()

		self.__nameFont = QtGui.QFont('Muli Light')
		self.__nameFont.setBold(True)
		# self.__nameFont.setPointSize(12)

		self.__macFont = QtGui.QFont('Muli Light')

		self.__iconConnected = QtGui.QPixmap(appCore.getIcon('check_icon.png'))

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

		if option.state & QtWidgets.QStyle.State_MouseOver:
			painter.fillRect(rectangle, self.__evenColor.lighter(120)) if isEvenNr else painter.fillRect(rectangle, self.__evenColor.lighter(120))

		elif option.state & QtWidgets.QStyle.State_Selected:
			print("selected olduk hanıım")

		elif option.state & QtWidgets.QStyle.State_Sunken:
			print("sunken olduk hanıım")

		else:
			painter.fillRect(rectangle, self.__evenColor) if isEvenNr else painter.fillRect(rectangle, self.__oddColor)

		iconRect = QtCore.QRect(option.rect.topLeft() + QtCore.QPoint(self.marginLeft(), self.marginTop()), QtCore.QPoint(option.rect.height() - self.__bottomMargin - self.__topMargin, option.rect.y() + option.rect.height() - self.__bottomMargin))
		connectionRect = QtCore.QRect(QtCore.QPoint(option.rect.width() - option.rect.height() / 5 * 3 - self.marginRight(), option.rect.y() + option.rect.height() / 5), QtCore.QPoint(option.rect.width() - self.marginRight(), option.rect.y() + option.rect.height() - option.rect.height() / 5))
		nameRect = QtCore.QRect(QtCore.QPoint(iconRect.topRight().x() + self.spacing(), iconRect.topRight().y() + 2), QtCore.QPoint(option.rect.width() - connectionRect.width() - self.spacing() - self.marginRight(), option.rect.y() + option.rect.height() / 2 - self.spacing() / 2))
		macRect = QtCore.QRect(QtCore.QPoint(iconRect.topRight().x() + self.spacing(), nameRect.bottomLeft().y() + self.spacing() - 3), QtCore.QPoint(option.rect.width() - connectionRect.width() - self.spacing() - self.marginRight(), option.rect.y() + option.rect.height() - self.marginBottom() - 5))

		iconToDraw = self.__iconUndefined
		if deviceType == DeviceTypes.EVC:
			iconToDraw = self.__iconEVC

		elif deviceType == DeviceTypes.UNDEFINED:
			iconToDraw = self.__iconUndefined

		elif deviceType == DeviceTypes.HEADPHONES:
			iconToDraw = self.__iconHeadphones

		elif deviceType == DeviceTypes.LAPTOP:
			iconToDraw = self.__iconLaptop

		elif deviceType == DeviceTypes.PHONE:
			iconToDraw = self.__iconPhone

		hCoefficient = iconToDraw.height() / iconRect.height()
		wCoefficient = iconToDraw.width() / iconRect.width()

		if hCoefficient > wCoefficient:
			width = iconToDraw.width() * iconRect.height() / iconToDraw.height()
			iconBoundingRect = QtCore.QRect((iconRect.width() - width) / 2 + iconRect.x(), iconRect.y(), width, iconRect.height())

		elif hCoefficient < 1 and wCoefficient < 1:
			iconBoundingRect = QtCore.QRect((iconRect.width() - iconToDraw.rect().width()) / 2 + iconRect.x(), (iconRect.height() - iconToDraw.rect().height()) / 2 + iconRect.y(), iconToDraw.rect().width(), iconToDraw.rect().height())

		else:
			height = iconToDraw.height() * iconRect.width() / iconToDraw.width()
			iconBoundingRect = QtCore.QRect(iconRect.x(), (iconRect.height() - height) / 2 + iconRect.y(), iconRect.width(), height)

		# painter.drawText(iconRect, 0, "icon\nhere")
		painter.drawPixmap(iconBoundingRect, iconToDraw)

		# painter.drawRect(iconRect)
		# painter.drawRect(connectionRect)
		# painter.drawRect(nameRect)
		# painter.drawRect(macRect)
		# painter.drawLine(QtCore.QPoint(0, option.rect.height() - 1 + option.rect.y()), QtCore.QPoint(option.rect.width(), option.rect.height() - 1 + option.rect.y()))

		painter.setFont(self.__nameFont)
		painter.drawText(nameRect, 0, fontMetrics.elidedText(deviceName, QtCore.Qt.ElideRight, nameRect.width()))
		painter.setFont(self.__macFont)
		painter.drawText(macRect, 0, fontMetrics.elidedText(deviceMac, QtCore.Qt.ElideRight, macRect.width()))

		if isDeviceConnected:
			painter.drawPixmap(connectionRect, self.__iconConnected)

		painter.restore()

	def sizeHint(self, option, index):
		return QtCore.QSize(option.rect.width(), 60)

	def setContentMargins(self, left, top, right, bottom):
		self.__leftMargin = int(left)
		self.__topMargin = int(top)
		self.__rightMargin = int(right)
		self.__bottomMargin = int(bottom)

	def setMarginLeft(self, marginLeft):
		self.__leftMargin = int(marginLeft)

	def setMarginTop(self, marginTop):
		self.__topMargin = int(marginTop)

	def setMarginRight(self, marginRight):
		self.__rightMargin = int(marginRight)

	def setMarginBottom(self, marginBottom):
		self.__bottomMargin = int(marginBottom)

	def contentMargins(self):
		return self.__leftMargin, self.__topMargin, self.__rightMargin, self.__bottomMargin

	def marginLeft(self):
		return self.__leftMargin

	def marginTop(self):
		return self.__topMargin

	def marginRight(self):
		return self.__rightMargin

	def marginBottom(self):
		return self.__bottomMargin

	def setSpacing(self, spacing):
		self.__spacing = int(spacing)

	def spacing(self):
		return self.__spacing

	def setPrimaryBackgroundColor(self, color):
		self.__evenColor = color

	def setSecondaryBackgroundColor(self, color):
		self.__oddColor = color

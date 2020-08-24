from PySide2 import QtCore
from models.devices import BaseDevice, EVCDevice, HeadphoneDevice, LaptopDevice, PhoneDevice


class ListModel(QtCore.QAbstractListModel):
	def __init__(self,  adapter = None, parent = None):
		super().__init__(parent)
		self.__deviceList = [EVCDevice.EVCDevice("am337x-evmsk", "CC:3F:48:SD:4R:77", True, "ok"), BaseDevice.BaseDevice("Unnamed", "XZ:4G:F3:F1:LF:55", False), PhoneDevice.PhoneDevice("iPhone", "KL:LF:D5:S2:TT:44", False), HeadphoneDevice.HeadphoneDevice("Beats JB", "X4:SF:AD:14:2G:WZ", False), LaptopDevice.LaptopDevice("Lenovo Laptop", "SG:LV:4L:X3:ZV:67", False)]
		self.__adapter = adapter

	def rowCount(self, index):
		# No regard to parent index
		return len(self.__deviceList)

	def index(self, row, column, parent = QtCore.QModelIndex()):
		if parent.isValid() or column != 0 or row > self.rowCount(parent):
			return QtCore.QModelIndex()

		content = self.__deviceList[row]
		return self.createIndex(row, column, content)

	def flags(self, index):
		return QtCore.Qt.ItemNeverHasChildren | \
			   QtCore.Qt.ItemIsDropEnabled

	def data(self, index, role = QtCore.Qt.DisplayRole):
		content = index.internalPointer()

		if role == QtCore.Qt.DisplayRole:
			return content.name()

		if role == QtCore.Qt.UserRole:
			return content

	def dataFromIndex(self, index):
		if not index.isValid() or index is None:
			return None

		return index.data(QtCore.Qt.UserRole)

	def indexFromData(self, data):
		if data is None:
			return QtCore.QModelIndex()

		rowNr = -1
		if data in self.__deviceList:
			rowNr = self.__deviceList.index(data)

		if rowNr < 0:
			return QtCore.QModelIndex()

		return self.createIndex(rowNr, 0, data)

	# Set self.__deviceList anew and reset model
	def setDevices(self, deviceList):
		self.beginResetModel()
		devices = deviceList
		if self.__adapter:
			devices = self.__adapter.request(deviceList)
		self.__deviceList = devices
		self.endResetModel()

	# Add one or more devices to model
	def addDevice(self, deviceList):
		self.beginInsertRows(QtCore.QModelIndex(), len(self.__deviceList), len(self.__deviceList) + len(devices) - 1)
		devices = deviceList
		if self.__adapter:
			devices = self.__adapter.request(deviceList)
		self.__deviceList = self.__deviceList + devices
		self.endInsertRows()

	# Remove one or more devices from model
	# TODO: INCOMPLETE
	def removeDevice(self, deviceList):
		index = self.indexFromData(deviceList)
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		self.__deviceList.remove(deviceList)
		self.endRemoveRows()

	def connectedDevice(self):
		connectedDevice = None
		for device in self.__deviceList:
			if device.isConnected():
				connectedDevice = device

		return connectedDevice

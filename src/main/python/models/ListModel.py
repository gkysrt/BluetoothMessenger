from PySide2 import QtCore
from models.devices import BaseDevice, EVCDevice, HeadphoneDevice, LaptopDevice, PhoneDevice
from models.Enum import DeviceTypes


class ListModel(QtCore.QAbstractListModel):
	def __init__(self,  adapter = None, parent = None):
		super().__init__(parent)
		self.__deviceList = [EVCDevice.EVCDevice("am337x-evmsk", "CC:3F:48:FD:4D:77", True, "ok"), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), PhoneDevice.PhoneDevice("iPhone", "41:AF:D5:S2:TT:44", False), HeadphoneDevice.HeadphoneDevice("Beats JB", "X4:SF:AD:14:2G:WZ", False), LaptopDevice.LaptopDevice("Lenovo Laptop", "SG:LV:4L:X3:ZV:67", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False), BaseDevice.BaseDevice("Unnamed", "BF:4C:F3:F1:DF:55", False)]
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

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		device = self.dataFromIndex(index)

		if role == QtCore.Qt.UserRole:
			if not isinstance(value, BaseDevice.BaseDevice):
				return False

			device.setName(value.name())
			device.setMac(value.mac())
			device.setDeviceClass(value.deviceClass())
			device.setConnected(value.isConnected())
			device.setServices(value.services())

			if value.deviceType() == DeviceTypes.EVC:
				device.setStatus(device.status())

			return True

		elif role == QtCore.Qt.EditRole:
			editType, editValue = value
			if editType == 'services':
				device.setServices(editValue)

			elif editType == 'mac':
				device.setMac(editValue)

			elif editType == 'name':
				device.setName(editValue)

			elif editType == 'deviceClass':
				device.setDeviceClass(editValue)

			elif editType == 'isConnected':
				device.setConnected(editValue)

			else:
				return False

			return True

		return False

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
		self.beginInsertRows(QtCore.QModelIndex(), len(self.__deviceList), len(self.__deviceList) + len(deviceList) - 1)
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

	# Returns devices in a list with given conditions
	def getFilteredDevices(self, **kwargs):
		name = kwargs.get('name', None)
		mac = kwargs.get('mac', None)
		deviceClass = kwargs.get('deviceClass', None)
		deviceType = kwargs.get('deviceType', None)

		filteredList = []
		for device in self.__deviceList:
			shouldAdd = True

			if name is not None and not name == device.name():
				shouldAdd = False

			if mac is not None and not mac == device.mac():
				shouldAdd = False

			if deviceClass is not None and not deviceClass == device.deviceClass():
				shouldAdd = False

			if deviceType is not None and not deviceType == device.deviceType():
				shouldAdd = False

			if shouldAdd:
				filteredList.append(device)

		return filteredList

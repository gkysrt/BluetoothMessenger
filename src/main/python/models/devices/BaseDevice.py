from models.Enum import DeviceTypes


class BaseDevice(object):
	def __init__(self, name = "", mac = "", deviceClass = 0, isConnected = False):
		super().__init__()
		self.__isConnected = isConnected
		self.__name = name
		self.__mac = mac
		self.__deviceClass = deviceClass

	def name(self):
		return self.__name

	def mac(self):
		return self.__mac

	def deviceClass(self):
		return self.__deviceClass

	def isConnected(self):
		return self.__isConnected

	def setName(self, name):
		self.__name = name

	def setMac(self, mac):
		self.__mac = mac

	def setMac(self, deviceClass):
		self.__deviceClass = deviceClass

	def setConnected(self, connected):
		self.__isConnected = bool(connected)

	@staticmethod
	def deviceType():
		return DeviceTypes.UNDEFINED

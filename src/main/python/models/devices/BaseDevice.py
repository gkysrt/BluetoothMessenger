from models.Enum import DeviceTypes


class BaseDevice(object):
	def __init__(self, name = "", mac = "", isConnected = False):
		super().__init__()
		self.__isConnected = isConnected
		self.__name = name
		self.__mac = mac

	def name(self):
		return self.__name

	def mac(self):
		return self.__mac

	def isConnected(self):
		return self.__isConnected

	def setName(self, name):
		self.__name = name

	def setMac(self, mac):
		self.__mac = mac

	def setConnected(self, connected):
		self.__isConnected = bool(connected)

	@staticmethod
	def deviceType():
		return DeviceTypes.UNDEFINED

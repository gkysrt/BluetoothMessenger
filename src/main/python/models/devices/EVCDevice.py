from models.devices import BaseDevice
from models.Enum import DeviceTypes


class EVCDevice(BaseDevice.BaseDevice):
	def __init__(self, name = "", mac = "", deviceClass = 0, isConnected = False, status = ""):
		super().__init__(name, mac, deviceClass, isConnected)
		self.__status = status

	def status(self):
		return self.__status

	def setStatus(self, status):
		self.__status = status

	@staticmethod
	def deviceType():
		return DeviceTypes.EVC

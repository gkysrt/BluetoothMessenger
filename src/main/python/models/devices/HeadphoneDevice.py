from models.devices import BaseDevice
from models.Enum import DeviceTypes


class HeadphoneDevice(BaseDevice.BaseDevice):
	def __init__(self, name = "", mac = "", deviceClass = 0, isConnected = False):
		super().__init__(name, mac, deviceClass, isConnected)

	@staticmethod
	def deviceType():
		return DeviceTypes.HEADPHONES

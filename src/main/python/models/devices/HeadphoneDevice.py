from models.devices import BaseDevice
from models.Enum import DeviceTypes


class HeadphoneDevice(BaseDevice.BaseDevice):
	def __init__(self, name = "", mac = "", isConnected = False):
		super().__init__(name, mac, isConnected)

	@staticmethod
	def deviceType():
		return DeviceTypes.HEADPHONES

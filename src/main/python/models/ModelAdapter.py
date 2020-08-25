# Adapter that is responsible for creating device objects from list elements and vice-versa
from models.devices import BaseDevice, EVCDevice, HeadphoneDevice, LaptopDevice, PhoneDevice


class ModelAdapter(object):
	def __init__(self):
		super().__init__()

	@classmethod
	def request(cls, inputList):
		outputList = []
		for _input in inputList:
			mac, name, deviceClass, services = _input
			outputList.append(BaseDevice.BaseDevice(name, mac, deviceClass, False))

		return outputList

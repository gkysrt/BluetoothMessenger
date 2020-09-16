import json
import BaseCommand
from PySide2 import QtWidgets, QtGui


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent=None):
        self.__onOffComboBox = None
        self.__startTime = None
        self.__endTime = None
        super().__init__(parent)

        self.initSignalsAndSlots()

    __options = ("-h", "-s", "-e", "-c", "--start", "--end", "--connector", "--help")
    __cmd = "eco-charge"
    __name = "Eco Charge"
    qss = """
            QLineEdit
            {
                color:rgb(64, 64, 64);
                border-radius: 2px;
                background-color: rgb(222, 222, 222);
                margin-left: 8px;
            }
            QLineEdit:focus
            {
                border: 1px solid rgb(40, 144, 229);
                background-color: rgb(240, 240, 240);
                color: rgb(40, 144, 229);
            }
            QLineEdit:disabled
            {
                border: 1px solid rgb(64, 64, 64);
                background-color: rgb(166, 166, 166);
            }
            QComboBox
            {
                border: none;
                background-color: rgb(200, 200, 200);
            }
            QComboBox::down-arrow
            {

            }
        """

    @classmethod
    def options(cls):
        return cls.__options

    @classmethod
    def command(cls):
        return cls.__cmd

    @classmethod
    def name(cls):
        return cls.__name

    @staticmethod
    def info():
        return """eco-charge [on/off] [options]: Eco-charge command, used with on/off arguments, start time and end times are given with option arguments
		OPTIONS:
			-h / --help: Show help
			-s / --start: Start time (In minutes)
			-e / --end: End time (In minutes)
			-c / --connector: Connector ID (default connector ID is 1)
		e.g
			eco-charge on -s 1320 -e 360 -c 1
		"""

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.__cmd, "result": "failed"}

        onOffArgument = argList.pop(0)
        startTime = 0
        endTime = 0
        connectorID = 1

        for i in range(len(argList)):
            if "-c" == argList[i] or "--connector" == argList[i]:
                if argList[i + 1]:
                    connectorID = int(argList[i + 1])
                    continue

            elif "-s" == argList[i] or "--start" == argList[i]:
                if argList[i + 1]:
                    startTime = int(argList[i + 1])
                    continue

            elif "-e" == argList[i] or "--end" == argList[i]:
                if argList[i + 1]:
                    endTime = int(argList[i + 1])
                    continue

        socket = kwargs.get('socket')
        print("Requesting echo charge: ", onOffArgument)

        try:
            if onOffArgument == "off":
                ecoChargeRequest = {"chargePoints": [{"connectorId": connectorID, "programs": [
                    {"key": "Charger.EVC.Program.EcoCharge", "value": "false"}]}]}
                socket.send(json.dumps(ecoChargeRequest).encode())
                return {"command": self.command(), "result": "successful"}

            elif onOffArgument == "on":
                ecoChargeRequest = {
                    "chargePoints": [{
                        "connectorId": connectorID,
                        "programs": [{
                            "key": "Charger.EVC.Program.EcoCharge",
                            "value": "true"
                        }],
                        "options": [
                            {
                                "key": "Charger.EVC.Option.EcoChargeStartTime",
                                "value": startTime
                            },
                            {
                                "key": "Charger.EVC.Option.EcoChargeStopTime",
                                "value": endTime
                            }]
                    }]
                }
                socket.send(json.dumps(ecoChargeRequest).encode())
                print("Eco charge is successfully requested {} with start time: {} end time: {}".format(onOffArgument,
                                                                                                        str(startTime),
                                                                                                        str(endTime)))
                return {"command": self.command(), "result": "successful"}

            else:
                raise Exception("Second argument should be on/off")

        except Exception as e:
            print("Failed to send eco-charge request: %s" % str(e))
            return {"command": self.command(), "result": "failed"}

    def executeUI(self, **kwargs):
        onOffArgument = "on"
        startTime = 0
        endTime = 0
        connectorID = 1

        socket = kwargs.get('socket')
        print("Requesting echo charge: ", onOffArgument)

        try:
            if onOffArgument.lower() == "off":
                ecoChargeRequest = {"chargePoints": [{"connectorId": connectorID, "programs": [
                    {"key": "Charger.EVC.Program.EcoCharge", "value": "false"}]}]}
                socket.send(json.dumps(ecoChargeRequest).encode())
                return {"command": self.command(), "result": "successful"}

            elif onOffArgument.lower() == "on":
                ecoChargeRequest = {
                    "chargePoints": [{
                        "connectorId": connectorID,
                        "programs": [{
                            "key": "Charger.EVC.Program.EcoCharge",
                            "value": "true"
                        }],
                        "options": [
                            {
                                "key": "Charger.EVC.Option.EcoChargeStartTime",
                                "value": startTime
                            },
                            {
                                "key": "Charger.EVC.Option.EcoChargeStopTime",
                                "value": endTime
                            }]
                    }]
                }
                socket.send(json.dumps(ecoChargeRequest).encode())
                print("Eco charge is successfully requested {} with start time: {} end time: {}".format(onOffArgument,
                                                                                                        str(startTime),
                                                                                                        str(endTime)))
                return {"command": self.command(), "result": "successful"}

            else:
                raise Exception("Second argument should be on/off")

        except Exception as e:
            print("Failed to send eco-charge request: %s" % str(e))
            return {"command": self.command(), "result": "failed"}

    def setupUi(self):
        self.setStyleSheet(self.qss)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        infoTextLabel = QtWidgets.QLabel(self)
        infoTextLabel.setText("Eco Charge command is used to charge EV between given time interval")
        infoTextLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        containerWidget = QtWidgets.QWidget(self)
        containerLayout = QtWidgets.QHBoxLayout(containerWidget)

        textEditWidget = QtWidgets.QWidget(containerWidget)
        textEditLayout = QtWidgets.QVBoxLayout(textEditWidget)

        startTimeWidget = QtWidgets.QWidget(textEditWidget)
        startTimeLayout = QtWidgets.QHBoxLayout(startTimeWidget)
        startTimeTextLabel = QtWidgets.QLabel(startTimeWidget)
        startTimeTextLabel.setText("Start Time:")
        startTimeTextLabel.setFixedWidth(80)
        self.__startTime = QtWidgets.QLineEdit(textEditWidget)
        self.__startTime.setPlaceholderText("Epoch Time")
        self.__startTime.setValidator(QtGui.QIntValidator(0, 2147483647))
        startTimeLayout.addWidget(startTimeTextLabel)
        startTimeLayout.addWidget(self.__startTime)

        endTimeWidget = QtWidgets.QWidget(textEditWidget)
        endTimeLayout = QtWidgets.QHBoxLayout(endTimeWidget)
        endTimeTextLabel = QtWidgets.QLabel(endTimeWidget)
        endTimeTextLabel.setText("End Time:")
        endTimeTextLabel.setFixedWidth(80)
        self.__endTime = QtWidgets.QLineEdit(textEditWidget)
        self.__endTime.setPlaceholderText("Epoch Time")
        self.__endTime.setValidator(QtGui.QIntValidator(0, 2147483647))
        endTimeLayout.addWidget(endTimeTextLabel)
        endTimeLayout.addWidget(self.__endTime)

        textEditLayout.addWidget(startTimeWidget)
        textEditLayout.addWidget(endTimeWidget)

        self.__onOffComboBox = QtWidgets.QComboBox(self)
        self.__onOffComboBox.addItem("On")
        self.__onOffComboBox.addItem("Off")
        self.__onOffComboBox.setFixedWidth(200)

        containerLayout.addWidget(self.__onOffComboBox)
        containerLayout.addWidget(textEditWidget)

        layout.addWidget(infoTextLabel)
        layout.addWidget(containerWidget)

    def initSignalsAndSlots(self):
        self.__onOffComboBox.currentTextChanged.connect(self.onComboBoxTextChange)

    def onComboBoxTextChange(self, text):
        if text.upper() == "ON":
            self.__startTime.setEnabled(True)
            self.__endTime.setEnabled(True)

        else:
            self.__startTime.setEnabled(False)
            self.__endTime.setEnabled(False)

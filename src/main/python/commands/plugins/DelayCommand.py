import json
import BaseCommand
from PySide2 import QtWidgets


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        self.__minutes = None
        self.__hours = None
        self.__seconds = None
        self.__onOffComboBox = None
        super().__init__(parent)

        self.initSignalsAndSlots()

    __options = ("-h", "-c", "-s", "-m", "-h", "--second", "--minute", "--hour", "--connector", "--help")
    __cmd = "delay-charge"
    __name = "Delay Charge"
    qss = """
        QLineEdit
        {
            border: 1px solid rgb(64, 64, 64);
            color:rgb(64, 64, 64);
            border-radius: 2px;
            background-color = rgb(92, 92, 92);
            margin-left: 8px;
        }
        QLineEdit:focus
        {
            border: 1px solid rgb(40, 144, 229);
            color: rgb(40, 144, 229);
        }
        QComboBox
        {
            border: none;
            background-color: rgb(128, 128, 128);
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
        return """delay-charge [on/off] [options]: Delay charge command, second arg on off, a delay amount should be specified
            OPTIONS:
                -h / --help: Show help
                -c / --connector: Connector ID (default connector ID is 1)
                -s / --second: Delay amount in seconds
                -m / --minute: Delay amount in minutes
                -h / --hour: Delay amount in hours
            e.g:
                delay-charge on -m 60 -c 1
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        delayEnabled = argList.pop(0)

        socket = kwargs.get('socket')
        connectorID = 1

        delayTime = 0
        timeUnit = "minute"

        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

        for i in range(len(argList)):
            if argList[i] == "-m" or argList[i] == "--minute":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    break

            elif argList[i] == "-h" or argList[i] == "--hour":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    delayTime = delayTime * 60
                    # timeUnit = "hour"
                    break

            elif argList[i] == "-s" or argList[i] == "--second":
                if argList[i + 1]:
                    delayTime = int(argList[i + 1])
                    # timeUnit = "second"
                    delayTime = delayTime / 60
                    break

        delayChargeRequest = None

        if delayEnabled == "on":
            # TODO: What is step, unit, min, max scale
            delayChargeRequest = {"chargePoints":
                [{
                    "connectorId": connectorID,
                    "programs":
                        [{"key": "Charger.EVC.Program.DelayCharge",
                          "value": "true"}],
                    "options": [{
                        "key": "Charger.EVC.Option.DelayChargeTime",
                        "valueType": "Integer",
                        "value": delayTime}
                    ]}
                ]}

        elif delayEnabled == "off":
            delayChargeRequest = {
                "chargePoints": [{
                    "connectorId": connectorID,
                    "programs": [{
                        "key": "Charger.EVC.Program.DelayCharge",
                        "value": "false"
                    }]
                }]
            }

        if delayChargeRequest:
            try:
                socket.send(json.dumps(delayChargeRequest).encode())
                print("Delay charge is successfully requested {}: {} minutes".format(delayEnabled, str(delayTime)))
                return {"command": self.command(), "result": "successful"}

            except Exception as e:
                print("Failed to send delay charge request: ", str(e))
                return {"command": self.command(), "result": "failed"}
        else:
            print('Second argument of delay-charge command is "on" or "off"')
            return {"command": self.command(), "result": "failed"}

    def executeUI(self, **kwargs):
        delayEnabled = self.__onOffComboBox.currentText()
        socket = kwargs.get('socket')
        connectorID = 1

        delayTime = 0
        timeUnit = "minute"
        delayChargeRequest = None

        if delayEnabled.lower() == "on":
            # TODO: What is step, unit, min, max scale
            delayChargeRequest = {"chargePoints":
                [{
                    "connectorId": connectorID,
                    "programs":
                        [{"key": "Charger.EVC.Program.DelayCharge",
                          "value": "true"}],
                    "options": [{
                        "key": "Charger.EVC.Option.DelayChargeTime",
                        "valueType": "Integer",
                        "value": delayTime}
                    ]}
                ]}

        elif delayEnabled.lower() == "off":
            delayChargeRequest = {
                "chargePoints": [{
                    "connectorId": connectorID,
                    "programs": [{
                        "key": "Charger.EVC.Program.DelayCharge",
                        "value": "false"
                    }]
                }]
            }

        try:
            socket.send(json.dumps(delayChargeRequest).encode())
            print("Delay charge is successfully requested {}: {} minutes".format(delayEnabled, str(delayTime)))
            return {"command": self.command(), "result": "successful"}

        except Exception as e:
            print("Failed to send delay charge request: ", str(e))
            return {"command": self.command(), "result": "failed"}

    def setupUi(self):
        self.setStyleSheet(self.qss)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        textEditWidget = QtWidgets.QWidget(self)
        textEditLayout = QtWidgets.QHBoxLayout(textEditWidget)

        self.__hours = QtWidgets.QLineEdit(textEditWidget)
        self.__hours.setPlaceholderText("Hour")
        self.__minutes = QtWidgets.QLineEdit(textEditWidget)
        self.__minutes.setPlaceholderText("Minute")
        self.__seconds = QtWidgets.QLineEdit(textEditWidget)
        self.__seconds.setPlaceholderText("Second")

        self.__onOffComboBox = QtWidgets.QComboBox(self)
        self.__onOffComboBox.addItem("On")
        self.__onOffComboBox.addItem("Off")

        textEditLayout.addWidget(self.__hours)
        textEditLayout.addWidget(self.__minutes)
        textEditLayout.addWidget(self.__seconds)

        layout.addWidget(textEditWidget)

    def initSignalsAndSlots(self):
        self.__onOffComboBox.currentTextChanged.connect(self.onComboBoxTextChange)

    def onComboBoxTextChange(self, text):
        if text.upper() == "ON":
            self.__hours.setEnabled(True)
            self.__minutes.setEnabled(True)
            self.__seconds.setEnabled(True)

        else:
            self.__hours.setEnabled(False)
            self.__minutes.setEnabled(False)
            self.__seconds.setEnabled(False)

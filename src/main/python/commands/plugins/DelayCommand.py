import json
import BaseCommand
from PySide2 import QtWidgets, QtGui


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        self.__minutes = None
        self.__hours = None
        self.__seconds = None
        self.__onOffComboBox = None
        super().__init__(parent)

        self.initSignalsAndSlots()

    __options = ("-c", "-s", "-m", "--second", "--minute", "--hour", "--connector")
    __cmd = "delay-charge"
    __name = "Delay Charge"
    qss = """
        QComboBox
        {
            border: none;
            background-color: rgb(200, 200, 200);
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
                -c / --connector: Connector ID (default connector ID is 1)
                -s / --second: Delay amount in seconds
                -m / --minute: Delay amount in minutes
                -h / --hour: Delay amount in hours
            e.g:
                delay-charge on -m 60 -c 1
            """

    def execute(self, argList, **kwargs):
        if not argList:
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
        connectorID = kwargs.get('connector', 1)
        hours, minutes, seconds = 0, 0, 0

        hoursText = self.__hours.text()
        minutesText = self.__minutes.text()
        secondsText = self.__seconds.text()

        if hoursText:
            hours = int(hoursText)

        if minutesText:
            minutes = int(self.__minutes.text())

        if secondsText:
            seconds = int(self.__seconds.text())

        # timeUnit is minute
        delayTime = hours * 60 + minutes + int(seconds/60)

        if delayEnabled.lower() == "on":
            value = "true"

        elif delayEnabled.lower() == "off":
            value = "false"
            delayTime = 0

        else:
            return {"command": self.command(), "result": "failed"}

        delayChargeRequest = {"chargePoints":
            [{
                "connectorId": connectorID,
                "programs":
                    [{"key": "Charger.EVC.Program.DelayCharge",
                      "value": value}],
                "options": [{
                    "key": "Charger.EVC.Option.DelayChargeTime",
                    "valueType": "Integer",
                    "value": delayTime}
                ]}
            ]}

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

        infoTextLabel = QtWidgets.QLabel(self)
        infoTextLabel.setText("Delay Charge command is used to schedule EVC for next charge")
        infoTextLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        containerWidget = QtWidgets.QWidget(self)
        containerLayout = QtWidgets.QHBoxLayout(containerWidget)

        textEditWidget = QtWidgets.QWidget(containerWidget)
        textEditLayout = QtWidgets.QVBoxLayout(textEditWidget)

        hourWidget = QtWidgets.QWidget(textEditWidget)
        hourLayout = QtWidgets.QHBoxLayout(hourWidget)
        hourLayout.setContentsMargins(0, 0, 0, 0)
        hourTextLabel = QtWidgets.QLabel(hourWidget)
        hourTextLabel.setText("Hour:")
        hourTextLabel.setFixedWidth(60)
        self.__hours = QtWidgets.QLineEdit(textEditWidget)
        self.__hours.setPlaceholderText("Hour")
        self.__hours.setValidator(QtGui.QIntValidator(0, 100))
        hourLayout.addWidget(hourTextLabel)
        hourLayout.addWidget(self.__hours)

        minuteWidget = QtWidgets.QWidget(textEditWidget)
        minuteLayout = QtWidgets.QHBoxLayout(minuteWidget)
        minuteLayout.setContentsMargins(0, 0, 0, 0)
        minuteTextLabel = QtWidgets.QLabel(minuteWidget)
        minuteTextLabel.setText("Minute:")
        minuteTextLabel.setFixedWidth(60)
        self.__minutes = QtWidgets.QLineEdit(textEditWidget)
        self.__minutes.setPlaceholderText("Minute")
        self.__minutes.setValidator(QtGui.QIntValidator(0, 60000))
        minuteLayout.addWidget(minuteTextLabel)
        minuteLayout.addWidget(self.__minutes)

        secondWidget = QtWidgets.QWidget(textEditWidget)
        secondLayout = QtWidgets.QHBoxLayout(secondWidget)
        secondLayout.setContentsMargins(0, 0, 0, 0)
        secondTextLabel = QtWidgets.QLabel(secondWidget)
        secondTextLabel.setText("Second:")
        secondTextLabel.setFixedWidth(60)
        self.__seconds = QtWidgets.QLineEdit(textEditWidget)
        self.__seconds.setPlaceholderText("Second")
        self.__seconds.setValidator(QtGui.QIntValidator(0, 360000))
        secondLayout.addWidget(secondTextLabel)
        secondLayout.addWidget(self.__seconds)

        textEditLayout.addWidget(hourWidget)
        textEditLayout.addWidget(minuteWidget)
        textEditLayout.addWidget(secondWidget)

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
            self.__hours.setEnabled(True)
            self.__minutes.setEnabled(True)
            self.__seconds.setEnabled(True)

        else:
            self.__hours.setEnabled(False)
            self.__minutes.setEnabled(False)
            self.__seconds.setEnabled(False)

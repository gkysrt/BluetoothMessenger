import BaseCommand
import json
from PySide2 import QtGui, QtWidgets


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-h", "-c", "--connector", "--help")
    __cmd = "interface-setting"
    __name = "Interface Setting"
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
        return """interface-setting [options]: Used to configure interface settings
            OPTIONS:
                -h / --help : Show help
                -c / --connector: Specify a connector ID (default connector ID is 1)
                -t / --timezone: Specify a timezone setting
                -l / --lockablecable: Turn lockable cable "on" or "off"
                -a / --availablecurrent: Adjust available current (unit is mA)
                -p / --plugcharge: Turn plug and charge setting "on" or "off" 
			e.g
            	interface-setting --timezone Europe/Istanbul --lockablecable on -a 20 -p on
            """

    def execute(self, argList, **kwargs):
        if '-h' in argList or '--help' in argList:
            print(self.info())
            return {"command": self.command(), "result": "failed"}

        socket = kwargs.get('socket')

        connectorID = 1
        timezone = None
        lockableCable = None
        availableCurrent = None
        plugCharge = None

        for i in range(len(argList)):
            if argList[i] == "-c" or argList[i] == "--connector":
                if argList[i + 1]:
                    connectorID = argList[i + 1]

            elif argList[i] == "-t" or argList[i] == "--timezone":
                if argList[i + 1]:
                    timezone = argList[i + 1]

            elif argList[i] == "-l" or argList[i] == "--lockablecable":
                if argList[i + 1]:
                    lockableCable = "true" if argList[i + 1] == "on" else "false"

            elif argList[i] == "-a" or argList[i] == "--availablecurrent":
                if argList[i + 1] and (6 <= int(argList[i + 1]) <= 32):
                    availableCurrent = int(argList[i + 1])

            elif argList[i] == "-p" or argList[i] == "--plugcharge":
                if argList[i + 1]:
                    plugCharge = "true" if argList[i + 1] == "on" else "false"

        if not timezone and not lockableCable and not availableCurrent and not plugCharge:
            print("Failed to request settings change, you must specify a setting change")
            return {"command": "interface-setting", "result": "failed"}

        # Body of settings request
        settingsRequest = {
            "chargePoints": [{
                "connectorId": connectorID,
            }],
        }

        # Settings list to be added to settings request
        settingsList = list()

        # Fill settingsList respective to existing commands
        if timezone:
            timezoneSetting = {
                "key": "Charger.EVC.Setting.Timezone",
                "value": str(timezone)
            }
            settingsList.append(timezoneSetting)

        if lockableCable:
            lockableCableSetting = {
                "key": "Charger.EVC.Setting.LockableCable",
                "value": lockableCable
            }
            settingsList.append(lockableCableSetting)

        if availableCurrent:
            availableCurrentSetting = {
                "key": "Charger.EVC.Setting.AvailableCurrent",
                "value": availableCurrent
            }
            settingsList.append(availableCurrentSetting)

        if plugCharge:
            plugChargeSetting = {
                "key": "Charger.EVC.Setting.PlugAndCharge",
                "value": plugCharge
            }
            settingsList.append(plugChargeSetting)

        # Add settingsList to dictionary inside settingsRequest
        settingsRequest.get("chargePoints")[0]["settings"] = settingsList

        try:
            socket.send(json.dumps(settingsRequest).encode())

        except Exception as e:
            print("Failed to send setting change request: ", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Settings change is requested")
        return {"command": self.command(), "result": "successful"}

    def executeUI(self, **kwargs):
        socket = kwargs.get('socket')

        connectorID = 1
        timezone = None
        lockableCable = None
        availableCurrent = None
        plugCharge = None

        if not timezone and not lockableCable and not availableCurrent and not plugCharge:
            print("Failed to request settings change, you must specify a setting change")
            return {"command": "interface-setting", "result": "failed"}

        # Body of settings request
        settingsRequest = {
            "chargePoints": [{
                "connectorId": connectorID,
            }],
        }

        # Settings list to be added to settings request
        settingsList = list()

        # Fill settingsList respective to existing commands
        if timezone:
            timezoneSetting = {
                "key": "Charger.EVC.Setting.Timezone",
                "value": str(timezone)
            }
            settingsList.append(timezoneSetting)

        if lockableCable:
            lockableCableSetting = {
                "key": "Charger.EVC.Setting.LockableCable",
                "value": lockableCable
            }
            settingsList.append(lockableCableSetting)

        if availableCurrent:
            availableCurrentSetting = {
                "key": "Charger.EVC.Setting.AvailableCurrent",
                "value": availableCurrent
            }
            settingsList.append(availableCurrentSetting)

        if plugCharge:
            plugChargeSetting = {
                "key": "Charger.EVC.Setting.PlugAndCharge",
                "value": plugCharge
            }
            settingsList.append(plugChargeSetting)

        # Add settingsList to dictionary inside settingsRequest
        settingsRequest.get("chargePoints")[0]["settings"] = settingsList

        try:
            socket.send(json.dumps(settingsRequest).encode())

        except Exception as e:
            print("Failed to send setting change request: ", str(e))
            return {"command": self.command(), "result": "failed"}

        print("Settings change is requested")
        return {"command": self.command(), "result": "successful"}

    def setupUi(self):
        self.setStyleSheet(self.qss)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        infoTextLabel = QtWidgets.QLabel(self)
        infoTextLabel.setText("EVC Interface Settings")
        infoTextLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        containerWidget = QtWidgets.QWidget(self)
        containerLayout = QtWidgets.QHBoxLayout(containerWidget)

        textEditWidget = QtWidgets.QWidget(containerWidget)
        textEditLayout = QtWidgets.QVBoxLayout(textEditWidget)

        hourWidget = QtWidgets.QWidget(textEditWidget)
        hourLayout = QtWidgets.QHBoxLayout(hourWidget)
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

import BaseCommand
import json


class Plugin(BaseCommand.BaseCommand):
    def __init__(self, parent = None):
        super().__init__(parent)

    __options = ("-h", "-c", "--connector", "--help")
    __cmd = "interface-setting"
    __name = "Interface Setting"

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
        pass

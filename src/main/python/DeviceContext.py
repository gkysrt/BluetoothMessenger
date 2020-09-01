from observer import BaseContext
from observer.BaseObserver import BaseObserver
from models.Enum import EVCStatus


class DeviceContext(BaseContext.BaseContext):
    def __init__(self):
        super().__init__()
        self.__observerDict = {}
        self.__stateDict = {}

    def attach(self, observer: BaseObserver, statusType: EVCStatus) -> None:
        if statusType not in self.__observerDict.keys():
            self.__observerDict[statusType] = [observer]

        else:
            observerList = self.__observerDict.get(statusType)
            observerList.append(observer)
            self.__observerDict[statusType] = observerList

    def detach(self, observer: BaseObserver, statusType: EVCStatus) -> None:
        if statusType not in self.__observerDict.keys():
            return
        else:
            observerList = self.__observerDict.get(statusType)
            observerList.remove(observer)
            self.__observerDict[statusType] = observerList

    def notify(self, key: EVCStatus = None) -> None:
        # Notify all observers
        if key is None:
            for key in self.__observerDict.keys():
                observerList = self.__observerDict.get(key)
                for observer in observerList:
                    observer.update(self.__stateDict.get(key))

        # Notify related observers
        elif key in self.__observerDict.keys():
            observerList = self.__observerDict.get(key)
            for observer in observerList:
                observer.update(self.__stateDict.get(key))

        else:
            return

    def setStateDict(self, stateDict):
        self.__stateDict = dict(stateDict)
        self.notify()

    def stateDict(self):
        return self.__stateDict

    def setState(self, state, key):
        self.__stateDict[key] = state
        self.notify(key)

    def state(self, key):
        return self.__stateDict.get(key)

    def reset(self):
        self.__stateDict = {}
from observer import BaseContext
from observer.BaseObserver import BaseObserver
from models.Enum import EVCStatus


class DeviceContext(BaseContext.BaseContext):
    def __init__(self):
        super().__init__()
        # observerDict is a dict of observers. Observers register here using connectorID's and state keys
        self.__observerDict = {}

        # state is a dict of dicts. Each connectorID is a key and there's a corresponding dict
        self.__state = {}

    def attach(self, observer: BaseObserver, key: object) -> None:
        if key not in self.__observerDict.keys():
            self.__observerDict[key] = observer

        else:
            observerList = self.__observerDict.get(key)
            observerList.append(observer)
            self.__observerDict[key] = observerList

    def detach(self, observer: BaseObserver, key: object) -> None:
        if key not in self.__observerDict.keys():
            return
        else:
            observerList = self.__observerDict.get(key)
            observerList.remove(observer)
            self.__observerDict[key] = observerList

    def notify(self, key: object, connectorID) -> None:
        # Notify related observers
        if key in self.__observerDict.keys():
            observerList = self.__observerDict.get((connectorID, key))
            for observer in observerList:
                observer.update(self.state(connectorID, key))
        else:
            return

    def setState(self, state, key, connectorID):
        connectorState = self.__state.get(connectorID)
        connectorState[key] = state
        self.notify(key, connectorID)

    def state(self, connectorID, state = None):
        connectorState = self.__state.get(connectorID)
        if state in connectorState.keys():
            return connectorState.get(state)
        return connectorState

    def reset(self):
        self.__state = {}

    def addChargePoint(self, connectorID, data = None):
        self.__state[connectorID] = {}

    def removeChargePoint(self, connectorID):
        self.__state.pop(connectorID)

    def chargePointState(self, connectorID):
        return self.__state.get(connectorID)

    def chargePointCount(self):
        return len(self.__state.keys())

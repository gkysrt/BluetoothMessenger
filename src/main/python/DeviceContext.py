from observer import BaseContext
from observer.BaseObserver import BaseObserver
from PySide2 import QtCore


class DeviceContext(BaseContext.BaseContext):

    chargePointAdded = QtCore.Signal(int)
    chargePointRemoved = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        # observerDict is a dict of observers. Observers register here using connectorID's and state keys
        self.__observerDict = {}

        # state is a dict of dicts. Each connectorID is a key and there's a corresponding dict
        self.__state = {}
        # {
        #     'connectorID':0
        #     'programs':[]
        #     'status':[]
        #     'settings':[]
        # }

    def attach(self, observer: BaseObserver, key: object) -> None:
        if key not in self.__observerDict.keys():
            self.__observerDict[key] = [observer]

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
            observerList = self.__observerDict.get(key)
            for observer in observerList:
                observer.update(connectorID = connectorID, key = key, value = self.state(key, connectorID))
        else:
            return

    def setState(self, state, key, connectorID):
        connectorState = self.__state.get(connectorID)
        connectorState[key] = state
        self.notify(key, connectorID)

    # state() returns desired 'status' with respect to given parameters.
    def state(self, state = None, connectorID = None):
        # If connectorID is given
        if connectorID is not None:
            if connectorID in self.__state.keys():
                connectorState = self.__state.get(connectorID)

                # Look for given state inside dict of given connectorID, if existent return specific status
                if state in connectorState.keys():
                    return connectorState.get(state)

                # If non-existent, return whole connectorID dict
                return connectorState

        # # If a state is given, return that state's all occurrences inside a list with their connectorIDs
        # elif state is not None:
        #     connectorIDs = self.__state.keys()
        #     returnList = []
        #     for connectorID in connectorIDs:
        #         connectorState = self.__state.get(connectorID)
        #         returnState = connectorState.get(state, {})
        #         returnDict = {
        #             'connectorID': connectorID,
        #             'status': returnState
        #         }
        #         returnList.append(returnDict)
        #
        #     return returnList

        return self.__state

    def reset(self):
        self.__state = {}

    def addChargePoint(self, connectorID, data = None):
        self.__state[connectorID] = {}
        self.chargePointAdded.emit(connectorID)

    def removeChargePoint(self, connectorID):
        self.__state.pop(connectorID)
        self.chargePointRemoved.emit(connectorID)

    def chargePointState(self, connectorID):
        return self.__state.get(connectorID)

    def chargePointCount(self):
        return len(self.__state.keys())

    def chargePoints(self):
        return self.__state.keys()

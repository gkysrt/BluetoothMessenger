from observer import BaseContext
from observer.BaseObserver import BaseObserver


class DeviceContext(BaseContext.BaseContext):
    def __init__(self):
        super().__init__()
        self.__observerList = []
        self.__state = None

    def attach(self, observer: BaseObserver) -> None:
        self.__observerList.append(observer)

    def detach(self, observer: BaseObserver) -> None:
        self.__observerList.remove(observer)

    def notify(self) -> None:
        for observer in self.__observerList:
            observer.update()

    def setState(self, state):
        self.__state = state
        self.notify()

    def state(self):
        return self.__state

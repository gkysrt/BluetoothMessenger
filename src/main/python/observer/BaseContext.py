from observer.BaseObserver import BaseObserver
from PySide2 import QtCore


class BaseContext(QtCore.QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        """
        The Subject interface declares a set of methods for managing subscribers.
        """

    def attach(self, observer: BaseObserver, key: object) -> None:
        """
        Attach an observer to the subject, with a related EVCStatus.
        """
        pass

    def detach(self, observer: BaseObserver, key: object) -> None:
        """
        Detach an observer from the subject, from a related EVCStatus.
        """
        pass

    def notify(self, key: object = None) -> None:
        """
        Notify all observers about an event, whenever a related EVCStatus changes.
        """
        pass

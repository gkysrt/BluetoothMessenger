from PySide2 import QtCore


class BaseObserver(QtCore.QObject):
    def __init__(self, parent = None):
        super().__init__(parent)

    """
    The Observer interface declares the update method, used by contexts.
    """

    def update(self, **kwargs) -> None:
        """
        Receive update from context
        """
        raise Exception("An observer should implement method: update()")

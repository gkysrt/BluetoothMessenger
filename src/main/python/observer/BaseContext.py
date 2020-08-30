from observer.BaseObserver import BaseObserver


class BaseContext(object):
    def __init__(self):
        super().__init__()
        """
        The Subject interface declares a set of methods for managing subscribers.
        """

    def attach(self, observer: BaseObserver) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    def detach(self, observer: BaseObserver) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

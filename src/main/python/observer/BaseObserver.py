from observer.BaseContext import BaseContext


class BaseObserver(object):
    """
    The Observer interface declares the update method, used by contexts.
    """

    def update(self, context: BaseContext) -> None:
        """
        Receive update from context
        """
        pass

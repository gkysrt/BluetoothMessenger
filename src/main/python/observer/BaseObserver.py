class BaseObserver(object):
    """
    The Observer interface declares the update method, used by contexts.
    """

    def update(self, context: object) -> None:
        """
        Receive update from context
        """
        raise Exception("An observer should implement method: update()")

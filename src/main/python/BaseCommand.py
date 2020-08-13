# Commands are implemented in a plugin fashion, every time a file inherits BaseCommand inside /commands file,
# it'll be added and evaluated as an argument


class BaseCommand(object):
    @classmethod
    def options(cls):
        """
        :param
        :return set
        options() function simply returns available options in type set.
        e.g set("-v", "-h", "-t")
        Returned set is used for displaying in manual and also crucial for predefining available options
        """
        raise Exception("Plugin inherits BaseCommand should return accepted option strings in type set")

    @classmethod
    def command(cls):
        """
        :param
        :return str
        command() function simply returns a distinct name for the argument to use.
        command() is used for comparing user input to command.
        """
        raise Exception("Plugin inherits BaseCommand should return a string to be used as argument")

    @classmethod
    def name(cls):
        """
        :param
        :return str
        name() function should simply return the name of plugin that'll be shown on display of UI.
        Override this function and return a string to name your command on UI.
        If not reimplemented, name will be blank.
        """
        return ''

    @staticmethod
    def info():
        """
        :param
        :return str
        info() function simply returns a description for the argument.
        This is optional.
        """

    def setupUi(self):
        """
        :param
        :return
        A free space is given inside command panel widget to override setupUi() method and fill free space.
        This way, visualization of plugin part is fully customizable. You can take inputs from user and
        use the given space freely. If setupUi() is not overridden and reimplemented, command will not be added
        to UI
        """

    def execute(self, argList, **kwargs):
        """
        :param list
        :return dict
        execute() function does what argument should do upon execution.
        argList is a list of strings, and it is in order which user typed in .
        String list is parsed string list of user input and sent by CommandParser.
        Default return type is dict.
        """
        raise Exception("Plugin inherits BaseCommand should implement an execute method")

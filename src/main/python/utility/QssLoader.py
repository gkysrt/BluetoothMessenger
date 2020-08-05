class QssLoader(object):
    def __init__(self, shouldParse = False):
        super(QssLoader, self).__init__()
        self.__shouldParse = shouldParse
        self.__qssFunctionDict = dict()

    def loadQss(self, qssPath):
        qssFile = None

        try:
            qssFile = open(qssPath)

        except FileNotFoundError as e:
            # TODO: Log print
            print("Error opening qss file: '{}' - {}".format(qssFile, str(e)))

        qssString = ""

        if qssFile:
            qssString = qssFile.read()

        if self.__shouldParse:
            qssString = self.parse(qssString)

        return qssString

    def setParseEnabled(self, enabled):
        self.__shouldParse = bool(enabled)

    def parse(self, qssString):
        # TODO: Parse qss string here
        return qssString

    def addFunction(self, key, func):
        self.__qssFunctionDict[key] = func

    def removeFunc(self, key):
        self.__qssFunctionDict.pop(key)

from ApplicationCore import ApplicationCore
import os


class QssLoader(object):
    def __init__(self, shouldParse = True):
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

    def parse(self, qss):
        # TODO: Betterment of this function is needed
        appCore = ApplicationCore.getInstance()

        # Replacement of some %....% strings is done before
        qss = qss.replace('%ICON_PATH%', appCore.iconPath())
        qss = qss.replace('%PLUGIN_PATH%', appCore.pluginPath())
        qss = qss.replace('%QSS_PATH%', appCore.qssPath())

        # Reading possible functions is done afterwards
        shouldRead = False
        functionString = ''
        commentLine = False

        # Get all functions inside qss e.g $join(%PATH%, add.svg);$
        for i in range(len(qss)):
            if qss.startswith('/*', i):
                commentLine = True

            elif qss.startswith('*/', i) and commentLine:
                commentLine = False

            if not commentLine:
                if qss.startswith('$', i):
                    if shouldRead:
                        splitString = functionString.split('(')
                        funcToUse = splitString[0]
                        parameterString = splitString[1]
                        parameters = parameterString.split(',')
                        parameters[-1] = parameters[-1].split(')')[0]

                        if funcToUse == 'join':
                            stringToReplace = QssLoader.join([param.replace(' ', '') for param in parameters])
                            qss = qss.replace('$' + functionString + '$', stringToReplace.replace('\\', '/'))

                        # .. Here other functions can be filled ..

                        # ----------------------------------------
                        functionString = ''

                    shouldRead = not shouldRead

                elif shouldRead:
                    functionString = functionString + qss[i]

        return qss

    def addFunction(self, key, func):
        self.__qssFunctionDict[key] = func

    def removeFunc(self, key):
        self.__qssFunctionDict.pop(key)

    # This function is called from Ive.qss with the same name with the usage of: $join(param1, param2, ...)$
    @staticmethod
    def join(pathList):
        joinedPath = ''
        for path in pathList:
            joinedPath = os.path.join(joinedPath, path)

        return joinedPath

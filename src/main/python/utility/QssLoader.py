from ApplicationCore import ApplicationCore


class QssLoader(object):
    def __init__(self):
        super(QssLoader, self).__init__()
        self.loadQss()

    @staticmethod
    def loadQss():
        appCore = ApplicationCore.getInstance()

        try:
            qssFile = open(appCore.getQss('DefaultStyle.qss'))

        except FileNotFoundError as e:
            print(e)

        return qssFile.read()

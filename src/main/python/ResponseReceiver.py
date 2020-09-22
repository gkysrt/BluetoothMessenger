from PySide2 import QtCore
from models import Thread
import time


class ResponseReceiver(QtCore.QObject):
    responseReceived = QtCore.Signal(object)

    def __init__(self, socket=None, parent = None):
        super().__init__(parent)
        self.__socket = socket  # Socket to listen to
        self.__workerThread = Thread.Thread(self)

    def initSignalsAndSlots(self):
        self.__workerThread.failed.connect(self.onWorkerThreadFail)
        self.__workerThread.successful.connect(self.onWorkerThreadSuccess)

    def receive(self):
        try:
            msg = str(self.__socket.recv(8192), 'utf8')
            self.responseReceived.emit(msg)
        # Whenever socket.recv() runs and there is no  message to get, recv raises an exception
        # that we dont want
        except Exception as e:
            pass
            # print("Receive encountered an error, ", str(e))

    def setSocket(self, socket):
        self.__socket = socket

    def getSocket(self):
        return self.__socket

    def isRunning(self):
        return self.__workerThread.isRunning()

    def start(self):
        if self.__socket:
            self.__socket.setblocking(True)
            self.__workerThread.start(self.receive, looping=True)

    def stop(self):
        self.__workerThread.breakLoop()

    def onWorkerThreadSuccess(self, returnValue):
        print(returnValue)

    def onWorkerThreadFail(self, exception):
        print(exception)

    def close(self):
        self.__workerThread.quit()
        self.__socket.close()

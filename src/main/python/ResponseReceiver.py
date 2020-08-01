import threading


class ResponseReceiver(threading.Thread):
    def __init__(self, socket=None):
        super(ResponseReceiver, self).__init__()
        self.__isRunning = False
        self.__socket = socket  # Socket to listen to

    def run(self):
        while self.__isRunning:
            try:
                # TODO: socket.recv() can't be killed on program exit, better fix needed
                msg = str(self.__socket.recv(4096), 'utf8')
                print("Received message from socket: %s" % msg)

            # Whenever socket.recv() runs and there is no  message to get, recv raises an exception
            # that we dont want
            except Exception as e:
                continue

    def setSocket(self, socket):
        self.__socket = socket

    def getSocket(self):
        return self.__socket

    def isRunning(self):
        return self.__isRunning

    def start(self):
        if self.__socket:
            self.__socket.setblocking(False)
            self.__isRunning = True
            return super().start()

    def stop(self):
        self.__isRunning = False
        if self.__socket:
            self.__socket.close()

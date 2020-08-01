import sys
import CommandParser
import bluetooth
import ResponseReceiver

if __name__ == '__main__':
    commandParser = CommandParser.CommandParser("EVC Bluetooth Messenger")
    print("EVC Bluetooth Messenger")
    print("--------------------------------")
    print("Type \"help\" to display manual and \"exit\" to quit program.")
    print()

    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    responseReceiver = ResponseReceiver.ResponseReceiver()

    while True:
        inputString = input("EVCBluetoothMessenger# ")

        if inputString == 'quit' or inputString == 'exit':
            socket.close()
            if responseReceiver.isRunning():
                responseReceiver.stop()
                responseReceiver.join()
            sys.exit()

        returnValue = commandParser.parse(str(inputString), socket=socket)

        if returnValue and returnValue.get("command") == "connect" and returnValue.get("result") == "successful":
            responseReceiver.setSocket(socket.dup())  # Give duplicate of socket that is used to send data
            if not responseReceiver.isRunning():
                responseReceiver.start()

        elif returnValue and returnValue.get("command") == "connect" and returnValue.get("result") == "failed":
            socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        elif returnValue and returnValue.get("command") == "disconnect" and returnValue.get("result") == "successful":
            socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            if responseReceiver.isRunning():
                responseReceiver.stop()

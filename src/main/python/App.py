import ApplicationCore
from widgets import MainWindow
from PySide2 import QtGui
import sys, os


if __name__ == '__main__':
    appctxt = ApplicationCore.ApplicationCore.getInstance()
    appctxt.app.setOrganizationName("Vestel")
    appctxt.app.setOrganizationDomain("vestel.com.tr")
    appctxt.app.setApplicationName("EVC Bluetooth Messenger")

    # Add custom font to application
    pathToFont = appctxt.get_resource('Muli-Light.ttf')
    QtGui.QFontDatabase.addApplicationFont(pathToFont)

    # Start main window
    window = MainWindow.MainWindow()
    window.setMinimumSize(960, 540)
    window.show()

    #TODO: to be deleted
    window.move(500, 300)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

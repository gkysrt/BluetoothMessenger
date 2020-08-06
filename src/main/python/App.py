import ApplicationCore
from widgets import MainWindow
import sys


if __name__ == '__main__':
    appctxt = ApplicationCore.ApplicationCore.getInstance()

    appctxt.app.setOrganizationName("Vestel")
    appctxt.app.setOrganizationDomain("vestel.com.tr")
    appctxt.app.setApplicationName("EVC Bluetooth Messenger")

    window = MainWindow.MainWindow()
    window.setMinimumSize(800, 450)
    window.show()

    #TODO: to be deleted
    window.move(500, 300)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

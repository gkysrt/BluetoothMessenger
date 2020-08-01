from fbs_runtime.application_context.PySide2 import ApplicationContext
# from fbs_runtime import application_context
from widgets import MainWindow
import sys


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow.MainWindow()
    window.setFixedSize(800, 450)
    window.show()

    #TODO: to be deleted
    window.move(500, 300)
    # print(application_context.is_frozen())

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

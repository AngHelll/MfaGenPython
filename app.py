import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from gui_app import Ui_MainWindow


class App_Mfa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App_Mfa, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = App_Mfa()
    Window.show()
    sys.exit(app.exec_())

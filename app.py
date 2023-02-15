import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from gui_app import Ui_MainWindow


class App_Mfa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App_Mfa, self).__init__(parent)
        self.setupUi(self)
        self.btn_generar.clicked.connect(self.fn_generar_totp)

    def fn_generar_totp(self):
        self.fn_validar_campos()

    def fn_validar_campos(self):
        input_text_account = self.inp_account.text()
        print(input_text_account)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = App_Mfa()
    Window.show()
    sys.exit(app.exec_())

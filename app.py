import datetime
import sys
import pyotp
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from gui_app import Ui_MainWindow


class App_Mfa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App_Mfa, self).__init__(parent)
        self.setupUi(self)
        self.btn_generar.clicked.connect(self.fn_generar_totp)

    def fn_generar_totp(self):
        if self.inp_shared_key.text() != "" and self.inp_account.text() != "":
            sharedKey = self.inp_shared_key.text()
            if True:
                totp = pyotp.TOTP(sharedKey)
                codigo = str(totp.now())
                self.lbl_totp.setText(codigo)
                time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
                self.lbl_time.setText(str(int(time_remaining)))
                position = self.tbw_hystoric.rowCount()
                self.tbw_hystoric.insertRow(position)
                self.tbw_hystoric.setItem(position, 0, QTableWidgetItem(str(datetime.datetime.now())))
                self.tbw_hystoric.setItem(position, 1, QTableWidgetItem(str(sharedKey)))
                self.tbw_hystoric.setItem(position, 2, QTableWidgetItem(str(codigo)))
                self.tbw_hystoric.setItem(position, 3, QTableWidgetItem(str(self.inp_account.text())))
            else:
                self.lbl_totp.setText("No has ingresado los campos requeridos")
        else:
            self.lbl_totp.setText("No has ingresado los campos requeridos")
    #


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = App_Mfa()
    Window.show()
    sys.exit(app.exec_())

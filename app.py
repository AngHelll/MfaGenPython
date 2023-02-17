import csv
import datetime
import os.path
import sys
import pyotp
import PyQt6
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from gui_app import Ui_MainWindow


class App_Mfa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App_Mfa, self).__init__(parent)
        self.setupUi(self)
        #Cargar datos desde datos.txt
        self.fn_insert_datos()
        #Enlace de boton a funcionalidad
        self.btn_generar.clicked.connect(self.fn_generar_totp)

    def fn_generar_totp(self):
        sharedKey = self.inp_shared_key.text()
        accountId = self.inp_account.text()
        if sharedKey != "" and accountId != "" and len(sharedKey) > 8:
            #Expresion regular a implementar
            if True:
                totp = pyotp.TOTP(sharedKey)
                codigo = str(totp.now())
                self.lbl_totp.setText(codigo)
                #tiempo para generar nuevo totp
                time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
                #imprmir totp en lbl
                self.lbl_time.setText(str(int(time_remaining)))
                #No duplicar valores en la tabla o archivo
                if not self.fn_buscar_registro(codigo, sharedKey):
                    self.fn_insert_on_table(codigo, sharedKey, accountId)
                    self.fn_guardar_datos()
            else:
                #Mensaje de error cuando no se cumple con expresion regular
                self.lbl_totp.setText("No has ingresado los campos requeridos")
        else:
            #Mensaje de error cuando no se llenan los cmapos
            self.lbl_totp.setText("No has ingresado los campos requeridos")

    def fn_insert_on_table(self, codigo, sharedKey, accountid):
        #Insertar siempre en posicion 0
        position = 0
        #Se asigna posicion donde se insertara el row
        self.tbw_hystoric.insertRow(position)
        #insercion de datos
        self.tbw_hystoric.setItem(position, 0, QTableWidgetItem(str(datetime.datetime.now())))
        self.tbw_hystoric.setItem(position, 1, QTableWidgetItem(sharedKey))
        self.tbw_hystoric.setItem(position, 2, QTableWidgetItem(accountid))
        self.tbw_hystoric.setItem(position, 3, QTableWidgetItem(str(codigo)))

    def fn_insert_datos(self):
        if os.path.isfile("datos.txt"):
            with open('datos.txt', 'r') as file:
                lines = file.readlines()

            # Configurar el número de filas y columnas en la tabla
            self.tbw_hystoric.setRowCount(len(lines))
            self.tbw_hystoric.setColumnCount(4)

            # Agregar los datos a la tabla
            for i, line in enumerate(lines):
                # Separar los datos por tab
                datos = line.strip().split('\t')

                # Agregar los datos a la tabla
                for j, dato in enumerate(datos):
                    self.tbw_hystoric.setItem(i, j, QTableWidgetItem(dato))

    def fn_guardar_datos(self):
        #abre o crea el archivo datos
        with open("datos.txt", "w", newline="") as archivo:
            writer = csv.writer(archivo, delimiter="\t")
            #ciclo para recorrer y almacenar todos los datos a guardar
            for row in range(self.tbw_hystoric.rowCount()):
                row_data = []
                #ciclo para recorrer columnas
                for column in range(self.tbw_hystoric.columnCount()):
                    item = self.tbw_hystoric.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                #Escribir en archivo
                writer.writerow(row_data)

    def fn_buscar_registro(self, b_codigo, b_sharedkey):
        flg = False
        #Ciclo para recorrer tabla y buscar coincidencias
        for fila in range(self.tbw_hystoric.rowCount()):
            code = self.tbw_hystoric.item(fila, 3).text()
            sharedkey = self.tbw_hystoric.item(fila, 1).text()
            if code == b_codigo and sharedkey == b_sharedkey:
                flg = True
                break
        return flg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = App_Mfa()
    Window.show()
    sys.exit(app.exec())

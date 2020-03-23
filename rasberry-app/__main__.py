from PyQt5 import QtWidgets, uic
import sys

app = QtWidgets.QApplication([])
win = uic.loadUi("form.ui")  # расположение вашего файла .ui

win.show()
sys.exit(app.exec())

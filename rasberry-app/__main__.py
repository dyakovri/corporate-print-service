import os
import sys
import psycopg2
from PyQt5 import QtWidgets, uic
import main_form

app = QtWidgets.QApplication([])
uiM = main_form.Ui_Form()


def ui_create():
    # win = uic.loadUi("form.ui")  # расположение вашего файла .ui
    win = QtWidgets.QWidget()
    uiM.setupUi(win)
    win.show()
    sys.exit(app.exec())

def db_test():
    conn = psycopg2.connect(host=os.getenv("DBHOST", "localhost"), port=os.getenv("DBPORT", "5432"),
                            dbname=os.getenv("DBNAME", "test"), user=os.getenv("DBUSER", "user"),
                            password=os.getenv("DBPASS", "*****"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM information_schema.tables;")
    print(cur.fetchall())


if __name__ == '__main__':
    # db_test()
    ui_create()

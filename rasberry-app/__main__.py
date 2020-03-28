import os

from PyQt5 import QtWidgets, uic
import sys
import psycopg2

app = QtWidgets.QApplication([])
win = uic.loadUi("form.ui")  # расположение вашего файла .ui
def db_test():
    conn = psycopg2.connect(host=os.getenv("DBHOST", "localhost"), port=os.getenv("DBPORT", "5432"),
                            dbname=os.getenv("DBNAME", "test"), user=os.getenv("DBUSER", "user"),
                            password=os.getenv("DBPASS", "*****"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM information_schema.tables;")
    print(cur.fetchall())


if __name__ == '__main__':
    # db_test()

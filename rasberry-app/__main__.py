import os
import sys
import psycopg2
from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QDialog

import main_form

app = QtWidgets.QApplication([])
uiM = main_form.Ui_Form()


def ui_create():
    # win = uic.loadUi("form.ui")  # расположение вашего файла .ui
    win = QtWidgets.QWidget()
    uiM.setupUi(win)
    win.show()
    sys.exit(app.exec())


def printer():
    printer = QPrinter(QPrinter.HighResolution)
    # printer.setFromTo(1, 3)
    # printer.setDoubleSidedPrinting(True)
    # printer.setDuplex(printer.DuplexLongSide)
    # printer.setPrintRange(printer.PageRange)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName("test_out.pdf")
    inputPdf = PdfFileReader(open("Клуб-У 36991-00-00РЭ_КЛУБ-У_изм275.pdf", "rb"))
    print(inputPdf.getNumPages())

    file = QFile("Клуб-У 36991-00-00РЭ_КЛУБ-У_изм275.pdf")
    file.open(QIODevice.ReadOnly)
    stream = QTextStream(file)
    content = stream.readAll()
    document = QTextDocument(content)
    document.print(printer)
    print("complite")
    # printDiag = QPrintDialog(printer)
    # # if (editor->textCursor().hasSelection())
    # # dialog.addEnabledOption(QAbstractPrintDialog::PrintSelection);
    # if printDiag.exec() != QDialog.Accepted:
    #     return


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

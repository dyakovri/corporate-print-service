import os
import sys
import re
from threading import Timer

import psycopg2
from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QFile, QIODevice, QTextStream, QStringListModel, QTimer
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QDialog

import main_form

app = QtWidgets.QApplication([])
uiM = main_form.Ui_Form()
screens = []


def ui_create():
    global screens
    # win = uic.loadUi("form.ui")  # расположение вашего файла .ui
    win = QtWidgets.QWidget()
    uiM.setupUi(win)
    screens = [uiM.Main, uiM.Main_2, uiM.Main_3, uiM.Main_4]
    uiM.btn_1.clicked.connect(open_screen_sign_in_on_stud)
    uiM.btn_2.clicked.connect(open_screen_sign_in_on_prof)
    uiM.btn_exit.clicked.connect(open_main_screen)
    uiM.btn_exit_2.clicked.connect(open_main_screen)
    uiM.line_last_name.textEdited.connect(last_name_validation_check)
    uiM.pushButton.clicked.connect(open_screen_main4)
    open_main_screen()
    # ui_main_form.btn_exin.clicked.connect(exit_page)
    win.show()
    sys.exit(app.exec())


def open_screen_sign_in_on_stud():
    hide_all_screens()
    uiM.Main_2.setVisible(True)
    uiM.line_number.setPlaceholderText("Номер студенческого")
    open_screen_main2()
    uiM.line_number.disconnect()
    uiM.line_number.textEdited.connect(stud_validation_check)
    uiM.sign_in.disconnect()
    uiM.sign_in.clicked.connect(db_check_stud)


def open_screen_sign_in_on_prof():
    hide_all_screens()
    uiM.Main_2.setVisible(True)
    uiM.line_number.setPlaceholderText("Номер профсоюзного билета")
    open_screen_main2()
    uiM.line_number.disconnect()
    uiM.line_number.textEdited.connect(prof_validation_check)


def open_screen_main2():
    uiM.line_number.setText("")
    uiM.line_last_name.setText("")
    uiM.status.setVisible(False)
    prof_validation_check.temp_text = ""
    uiM.btn_exit.setVisible(True)


def db_check_stud():
    # TODO если не найден в базе или не зарегистрирован показать сообщение
    uiM.status.setText("Неверный номер или фамилия")
    uiM.status.setVisible(True)
    # Если база ответила положительно, то переключить на экран с работой
    open_screen_main3()


def open_screen_main3():
    hide_all_screens()
    uiM.Main_3.setVisible(True)
    uiM.listView.setModel(QStringListModel(get_files()))


def open_screen_main4():
    hide_all_screens()
    uiM.Main_4.setVisible(True)
    uiM.btn_exit.setVisible(False)
    t = Timer(10, open_main_screen)
    t.start()
    # timer_painter = QTimer()
    # timer_painter.start(1)
    # timer_painter.timeout.connect(open_main_screen)



def stud_validation_check():
    if re.match(r"^\d*$", uiM.line_number.text()) is None:
        uiM.line_number.setText(stud_validation_check.temp_text)
    stud_validation_check.temp_text = uiM.line_number.text()


stud_validation_check.temp_text = ""


def prof_validation_check():
    if re.match(r"^\d{0,6}$", uiM.line_number.text()) is None:
        uiM.line_number.setText(prof_validation_check.temp_text)
    prof_validation_check.temp_text = uiM.line_number.text()


prof_validation_check.temp_text = ""


def last_name_validation_check():
    if re.match(r"^[А-Яа-яЁё]*$", uiM.line_last_name.text(), re.I) is None:
        uiM.line_last_name.setText(last_name_validation_check.temp_text)
    last_name_validation_check.temp_text = uiM.line_last_name.text()


last_name_validation_check.temp_text = ""


def open_main_screen():
    hide_all_screens()
    uiM.Main.setVisible(True)
    uiM.btn_exit.setVisible(False)


def hide_all_screens():
    for v in screens:
        v.setVisible(False)


def get_files():
    path = "e:/"
    out = []
    files_count = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            files_count += 1
            if re.search(r"\.pdf$", f, re.I | re.UNICODE) is not None:
                out.append(f)
    out.sort()
    out.append("и других файлов: " + str(files_count))
    return out


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
    get_files()
    # db_test()
    ui_create()

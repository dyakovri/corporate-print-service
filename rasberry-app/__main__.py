import os
import re
import sys

from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QIODevice, QTextStream, QStringListModel, QTimer, QRegularExpression
from PyQt5.QtGui import QTextDocument, QRegularExpressionValidator
from PyQt5.QtPrintSupport import QPrinter

import db_controller
import main_form
import virtual_keyboard

app = QtWidgets.QApplication([])
uiM = main_form.Ui_Form()
screens = []
logoff_timer = QTimer()


def ui_create():
    global screens
    # win = uic.loadUi("form.ui")  # расположение вашего файла .ui
    win = QtWidgets.QWidget()
    uiM.setupUi(win)
    screens = [uiM.Main, uiM.Main_2, uiM.Main_3, uiM.Main_4, uiM.Main_5, uiM.Splash]
    uiM.btn_prof_login.clicked.connect(lambda: open_screen_sign_in(3))
    uiM.btn_stud_login.clicked.connect(lambda: open_screen_sign_in(4))
    uiM.btn_3.clicked.connect(open_screen_file_code)
    uiM.line_file_code.setPlaceholderText("Код файла")
    uiM.line_file_code.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d*$")))
    uiM.btn_exit.clicked.connect(open_main_screen)
    uiM.btn_exit_2.clicked.connect(open_screen_splash)
    uiM.btn_back.clicked.connect(open_screen_main3)
    uiM.line_last_name.setValidator(QRegularExpressionValidator(QRegularExpression(r"^[А-Яа-яЁё]*$")))
    uiM.pushButton.clicked.connect(open_screen_main4)
    virtual_keyboard.create_keyboard(uiM)
    open_main_screen()
    # ui_main_form.btn_exin.clicked.connect(exit_page)
    win.show()
    sys.exit(app.exec())


def open_screen_sign_in(type_id):
    hide_all_screens()
    uiM.Main_2.setVisible(True)
    open_screen_main2()
    uiM.line_number.disconnect()
    uiM.sign_in.disconnect()
    uiM.sign_in.clicked.connect(lambda: db_check_login(type_id))
    if type_id == 3:
        uiM.line_number.setPlaceholderText("Номер профсоюзного билета")
        uiM.line_number.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d{0,6}$")))
    elif type_id == 4:
        uiM.line_number.setPlaceholderText("Номер студенческого")
        uiM.line_number.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d*$")))


def open_screen_file_code():
    hide_all_screens()
    uiM.Main_5.setVisible(True)
    uiM.btn_exit.setVisible(True)
    uiM.status_2.setVisible(False)


def open_screen_main2():
    uiM.line_number.setText("")
    uiM.line_last_name.setText("")
    uiM.status.setVisible(False)
    uiM.btn_exit.setVisible(True)


def db_check_login(type_id):
    if uiM.line_last_name.text() == "" or uiM.line_number.text() == "":
        uiM.status.setText("Введи достаточно данных")
        uiM.status.setVisible(True)
        return
    out = db_controller.sign_in_routine(type_id, uiM.line_last_name.text(), uiM.line_number.text())
    if out is None or out[0][0] == 201:
        uiM.status.setText("Неверная пара номер фамилия или вы не являетесь подтвержденным пользователем")
        uiM.status.setVisible(True)
        return
    elif out[0][0] == 202:
        open_screen_main3()


def open_screen_main3():
    hide_all_screens()
    uiM.Main_3.setVisible(True)
    uiM.listView.setModel(QStringListModel(get_files()))
    logoff_timer.start(30000)


def open_screen_main4():
    hide_all_screens()
    uiM.Main_4.setVisible(True)
    uiM.btn_exit.setVisible(False)
    logoff_timer.start(12000)


def open_screen_splash():
    hide_all_screens()
    uiM.Splash.setVisible(True)
    logoff_timer.start(4000)


def open_main_screen():
    hide_all_screens()
    uiM.Main.setVisible(True)
    uiM.btn_exit.setVisible(False)
    logoff_timer.stop()


def hide_all_screens():
    for v in screens:
        v.setVisible(False)


def get_files():
    # path = "/media/pi/" # raspberry pi
    path = "e:/"  # win testing
    out = []
    files_count = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            files_count += 1
            if re.search(r"\.pdf$", f, re.I | re.UNICODE) is not None:
                out.append(os.path.join(root, f))
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
    print("complete")
    # printDiag = QPrintDialog(printer)
    # # if (editor->textCursor().hasSelection())
    # # dialog.addEnabledOption(QAbstractPrintDialog::PrintSelection);
    # if printDiag.exec() != QDialog.Accepted:
    #     return


if __name__ == '__main__':
    logoff_timer.setInterval(1)
    logoff_timer.timeout.connect(open_main_screen)
    # db_controller.db_test()
    ui_create()

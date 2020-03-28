# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 320)
        self.Main = QtWidgets.QWidget(Form)
        self.Main.setEnabled(True)
        self.Main.setGeometry(QtCore.QRect(0, 0, 480, 320))
        self.Main.setAutoFillBackground(True)
        self.Main.setObjectName("Main")
        self.btn_1 = QtWidgets.QPushButton(self.Main)
        self.btn_1.setGeometry(QtCore.QRect(60, 90, 100, 100))
        self.btn_1.setObjectName("btn_1")
        self.btn_2 = QtWidgets.QPushButton(self.Main)
        self.btn_2.setGeometry(QtCore.QRect(190, 90, 100, 100))
        self.btn_2.setObjectName("btn_2")
        self.btn_3 = QtWidgets.QPushButton(self.Main)
        self.btn_3.setGeometry(QtCore.QRect(330, 90, 100, 100))
        self.btn_3.setObjectName("btn_3")
        self.Main_2 = QtWidgets.QWidget(Form)
        self.Main_2.setEnabled(True)
        self.Main_2.setGeometry(QtCore.QRect(0, 0, 480, 320))
        self.Main_2.setAutoFillBackground(True)
        self.Main_2.setObjectName("Main_2")
        self.btn_exit = QtWidgets.QPushButton(self.Main_2)
        self.btn_exit.setGeometry(QtCore.QRect(429, 0, 51, 41))
        self.btn_exit.setObjectName("btn_exit")
        self.line_number = QtWidgets.QLineEdit(self.Main_2)
        self.line_number.setGeometry(QtCore.QRect(110, 90, 251, 31))
        self.line_number.setInputMask("")
        self.line_number.setText("")
        self.line_number.setPlaceholderText("")
        self.line_number.setObjectName("line_number")
        self.line_last_name = QtWidgets.QLineEdit(self.Main_2)
        self.line_last_name.setGeometry(QtCore.QRect(110, 160, 251, 31))
        self.line_last_name.setObjectName("line_last_name")
        self.sign_in = QtWidgets.QPushButton(self.Main_2)
        self.sign_in.setGeometry(QtCore.QRect(200, 240, 80, 22))
        self.sign_in.setObjectName("sign_in")
        self.status = QtWidgets.QLabel(self.Main_2)
        self.status.setGeometry(QtCore.QRect(110, 210, 251, 20))
        self.status.setObjectName("status")
        self.line_number.raise_()
        self.line_last_name.raise_()
        self.sign_in.raise_()
        self.status.raise_()
        self.btn_exit.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_1.setText(_translate("Form", "styd"))
        self.btn_2.setText(_translate("Form", "prof"))
        self.btn_3.setText(_translate("Form", "key_id"))
        self.btn_exit.setText(_translate("Form", "X"))
        self.line_last_name.setPlaceholderText(_translate("Form", "Last name"))
        self.sign_in.setText(_translate("Form", "sign in"))
        self.status.setText(_translate("Form", "TextLabel"))

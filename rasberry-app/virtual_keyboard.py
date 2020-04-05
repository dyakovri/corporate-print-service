from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

keys = list(map(chr, range(ord('а'), ord('я') + 1))) \
       + list(map(str, range(1, 9))) \
       + ['0', 'back']

_uiM = None


def create_keyboard(uiM):
    global _uiM
    _uiM = uiM
    for i, key in enumerate(keys):
        button = QtWidgets.QPushButton(str(key))
        button.setFixedSize(30, 30)
        button.setFocusPolicy(Qt.NoFocus)
        _uiM.numerkKeyboard.addWidget(button, i / 10, i % 10)
        button.clicked.connect(print_key(key))


def print_key(key):
    def out():
        line = None
        valid = QRegularExpressionValidator()
        if _uiM.line_number.hasFocus():
            line = _uiM.line_number
            valid.setRegularExpression(QRegularExpression(r"^\d*$"))
        elif _uiM.line_file_code.hasFocus():
            line = _uiM.line_file_code
            valid.setRegularExpression(QRegularExpression(r"^\d*$"))
        elif _uiM.line_last_name.hasFocus():
            line = _uiM.line_last_name
            valid.setRegularExpression(QRegularExpression(r"^[А-Яа-яЁё]*$"))
        if line is not None:
            if key == 'back':
                line.setText(line.text()[:-1])
            elif valid.validate(key, 0)[0] == 2:
                line.setText(line.text() + key)

    return out


def test_create_keyboard(uiM):
    for i in range(4):
        for j in range(3):
            button = QtWidgets.QPushButton(str(3 * i + j + 1))
            if 3 * i + j + 1 == 10:
                button = QtWidgets.QPushButton("0")
            elif 3 * i + j + 1 == 11:
                button = QtWidgets.QPushButton("back")
            elif 3 * i + j + 1 > 11:
                return
            uiM.numerkKeyboard.addWidget(button, i, j)
            button.setFocusPolicy(Qt.NoFocus)

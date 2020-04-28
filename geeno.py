import sys
from PyQt5 import QtWidgets

# NOW WITH CLASSES!


class Window(QtWidgets):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.btn1 = QtWidgets.QPushButton("Push Me")
        self.lbl1 = QtWidgets.QLabel("I'm a label")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.lbl1)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()

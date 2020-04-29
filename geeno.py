import sys
from PyQt5 import QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Geeno")
        h_box = QtWidgets.QHBoxLayout()
        v_box = QtWidgets.QVBoxLayout()

        self.title = QtWidgets.QLabel("Welcome to Geeno!")
        self.ageLbl = QtWidgets.QLabel("Age: ")
        self.ageEntry = QtWidgets.QLineEdit()
        self.heightLbl = QtWidgets.QLabel("Height: ")
        self.heightEntry = QtWidgets.QLineEdit()
        self.weightLbl = QtWidgets.QLabel("Weight: ")
        self.weightEntry = QtWidgets.QLineEdit()
        self.sexLbl = QtWidgets.QLabel("Sex: ")
        self.calcBtn = QtWidgets.QPushButton("Results")

        # Entries go here

        # Layout
        v_box.addWidget(self.title)
        v_box.addStretch()
        v_box.addWidget(self.ageLbl)
        v_box.addWidget(self.ageEntry)
        v_box.addStretch()
        v_box.addWidget(self.heightLbl)
        v_box.addWidget(self.heightEntry)
        v_box.addStretch()
        v_box.addWidget(self.weightLbl)
        v_box.addWidget(self.weightEntry)
        v_box.addStretch()
        v_box.addWidget(self.sexLbl)
        v_box.addStretch()
        v_box.addWidget(self.calcBtn)

        h_box.addLayout(v_box)
        self.setLayout(h_box)
        
        self.calcBtn.clicked.connect(self.getResults)
        self.show()

    def getResults(self):
       self.results = QtWidgets.QLabel("Results")
       v_box.addStretch()
       v_box.addWidget(self.results)

app = QtWidgets.QApplication(sys.argv)
geeno_window = Window()
sys.exit(app.exec_())
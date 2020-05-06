import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Geeno")
        # actions
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(self.close)
        quitAction.setShortcut(QtGui.QKeySequence("Ctrl+q"))

        # menu
        menu = self.menuBar()
        file_menu = menu.addMenu(u"&File")
        file_menu.addSeparator()
        file_menu.addAction(quitAction)

        self.init_UI()

    def init_UI(self):
        self.layout = QStackedLayout()
        self.calcPage = self.init_calcPage()
        self.resultPage = self.init_resultPage()
        self.layout.addWidget(self.calcPage)
        self.layout.addWidget(self.resultPage)

        self.layout.setCurrentWidget(self.calcPage)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def init_calcPage(self):
        layout = QGridLayout()
        lblTitle = QLabel("Please insert input: ")
        layout.addWidget(lblTitle, 0, 3)
        lblAge = QLabel("Date of birth: ")
        layout.addWidget(lblAge, 1, 0)
        lblHeight = QLabel("Heigth: ")
        layout.addWidget(lblHeight, 2, 0)
        lblWeight = QLabel("Weight: ")
        layout.addWidget(lblWeight, 3, 0)
        lblSex = QLabel("Sex: ")
        layout.addWidget(lblSex, 4, 0)


        goToResults = QPushButton("Results")
        goToResults.clicked.connect(lambda: self.layout.setCurrentWidget(self.resultPage))
        layout.addWidget(goToResults, 5,2)

        calcPage = QWidget()
        calcPage.setLayout(layout)

        return calcPage

    def init_resultPage(self):

        layout = QGridLayout()
        layout.addWidget(QLabel("I'm the second page"), 2,2)

        resultPage = QWidget()
        resultPage.setLayout(layout)

        return resultPage



app = QApplication(sys.argv)
geeno = MainWindow()
geeno.show()
app.exec_()

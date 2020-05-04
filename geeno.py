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
        self.calcPage = CalcPage()
        self.resultPage = ResultPage()

        self.pages = QStackedWidget(self)
        self.pages.addWidget(self.calcPage)
        self.pages.addWidget(self.resultPage)
        self.setCentralWidget(self.pages)
        self.pages.setCurrentWidget(self.calcPage)


class CalcPage(QWidget):
    def __init__(self):
        super(CalcPage, self).__init__()
        btn = QPushButton("Result")


class ResultPage(QWidget):
    def __init__(self):
        super(ResultPage, self).__init__()


app = QApplication(sys.argv)
geeno = MainWindow()
geeno.show()
app.exec_()

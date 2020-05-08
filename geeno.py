import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtGui

def error_message():
	msg = QMessageBox()
	msg.setText("Invalid Input")
	msg.setInformativeText("Please insert a valid input.")
	msg.setWindowTitle("Error")
	msg.exec_()

def getAge(birthday):
	now = QDate.currentDate()
	age = now.year() - birthday.year()

	if birthday.month() > now.month():
		age = age-1
	elif (birthday.month() == now.month()) and (birthday.day() > now.day()):
		age = age - 1
	return age

def getBmi(w, h):
    return round(w / h**2 * 10000, 1)

def getBmr(age, sex, w, h):
    if sex == 'M':
        bmr = 66.473 + 13.7156 * w + 5.0033 * h - 6.755 * age
    elif sex == 'F':
        bmr = 655.095 + 9.5634 * w + 1.849 * h - 4.6756 * age
    else:
        bmr = -1
    return round(bmr, 2)

def getBmiRange(bmi):
	if bmi < 18.5:
		return "Underweiight"
	elif bmi < 25:
		return "Healthy weight"
	elif bmi < 30:
		return "Overweight"
	elif bmi < 35:
		return "Obese 1"
	elif bmi < 40:
		return "Obese 2"
	else:
		return "Obese 3"


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
		self.setStyleSheet(open("styles.css").read())
	def init_UI(self):


		self.layout = QStackedLayout()
		self.calcPage = self.init_calcPage()
		#self.resultPage = self.init_resultPage()
		self.layout.addWidget(self.calcPage)
		#self.layout.addWidget(self.resultPage)

		self.layout.setCurrentWidget(self.calcPage)

		widget = QWidget()
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)

	def init_calcPage(self):
		self.setGeometry(300, 100, 400, 200)
		layout = QGridLayout()
		lblWelcome = QLabel("GEENO Calculator")
		layout.addWidget(lblWelcome, 0,2)
		lblTitle = QLabel("Please insert input: ")
		layout.addWidget(lblTitle, 1, 0)

		# date of birth
		lblAge = QLabel("Date of birth: ")
		layout.addWidget(lblAge, 2, 0)
		self.entryAge = QDateEdit()
		self.entryAge.setDate(QDate.currentDate())
		self.entryAge.setDisplayFormat("dd/MM/yyyy")
		layout.addWidget(self.entryAge, 2, 1)

		# height
		lblHeight = QLabel("Heigth: ")
		layout.addWidget(lblHeight, 3, 0)
		self.entryHeight = QLineEdit()
		self.entryHeight.setValidator(QtGui.QIntValidator())
		self.entryHeight.setMaxLength(3)
		layout.addWidget(self.entryHeight, 3, 1)


		# weight
		lblWeight = QLabel("Weight: ")
		layout.addWidget(lblWeight, 4, 0)
		self.entryWeight = QLineEdit()
		self.entryWeight.setValidator(QtGui.QDoubleValidator())
		layout.addWidget(self.entryWeight, 4, 1)

		# sex
		lblSex = QLabel("Sex: ")
		layout.addWidget(lblSex, 5, 0)
		self.entrySexM = QRadioButton("M")
		layout.addWidget(self.entrySexM, 5, 1)
		self.entrySexF = QRadioButton("F")
		layout.addWidget(self.entrySexF, 5, 2)

		# laf
		lblLaf = QLabel("LAF: ")
		layout.addWidget(lblLaf, 6, 0)
		self.entryLaf = QLineEdit()
		self.entryLaf.setValidator(QtGui.QDoubleValidator())
		layout.addWidget(self.entryLaf, 6, 1)


		self.clearAllBtn = QPushButton("Clear")
		self.clearAllBtn.clicked.connect(lambda: self.clearAll())
		layout.addWidget(self.clearAllBtn, 7, 1)
		self.goToResults = QPushButton("Results")
		self.goToResults.clicked.connect(lambda: self.getInput())
		self.goToResults.setAutoDefault(True)
		layout.addWidget(self.goToResults, 7, 2)

		calcPage = QWidget()
		calcPage.setLayout(layout)

		return calcPage

	def init_resultPage(self):
		layout = QGridLayout()

		layout.addWidget(QLabel("Patient Info"), 0, 0)
		layout.addWidget(QLabel("Results"), 0, 1)
		lblBirthDay = QLabel("Birthday: " + self.birthday.toString('d/MM/yyyy'))
		layout.addWidget(lblBirthDay, 1, 0)
		lblAge = QLabel("Age: "+str(self.age))
		layout.addWidget(lblAge, 2, 0)
		lblHeight = QLabel("Height: "+self.height)
		layout.addWidget(lblHeight, 3, 0)
		lblWeight = QLabel("Weight: "+self.weight)
		layout.addWidget(lblWeight, 4, 0)
		lblSex = QLabel("Sex: "+self.sex)
		layout.addWidget(lblSex, 5, 0)
		lblLaf = QLabel("LAF: " + str(self.laf))
		layout.addWidget(lblLaf, 6, 0)
		# BMR
		bmr = getBmr(int(self.age), self.sex,  float(self.weight), int(self.height))
		lblBmr = QLabel("bmr: "+ str(bmr))
		layout.addWidget(lblBmr, 1, 1)
		# BMI
		bmi = getBmi(float(self.weight), int(self.height))
		lblBmi = QLabel("bmi: " + str(bmi))
		layout.addWidget(lblBmi, 2, 1)
		lblBmiRange = QLabel("The patient is in the following range: "+str(getBmiRange(bmi)))
		layout.addWidget(lblBmiRange, 3, 1)

		# TEE (Total Energy Expenditure (?))
		layout.addWidget(QLabel("TEE: "+str(bmr*float(self.laf))), 4, 1 )
		layout.addWidget(QLabel("Thank you for using geeno!"), 7,0)


		self.goBackBtn = QPushButton("Go Back")
		self.goBackBtn.clicked.connect(lambda: self.goBack())
		layout.addWidget(self.goBackBtn, 8, 0)

		exitBtn = QPushButton("Quit")
		exitBtn.clicked.connect(self.close)
		layout.addWidget(exitBtn, 8, 1)

		resultPage = QWidget()
		resultPage.setLayout(layout)

		return resultPage

	def getInput(self):
		try:
			self.birthday = self.entryAge.date()
			self.age = getAge(self.birthday)
			self.height = self.entryHeight.text()
			self.weight = self.entryWeight.text()
			if self.entrySexM.isChecked():
				self.sex = 'M'
			else:
				self.sex = 'F'
			self.laf = self.entryLaf.text()
			try:
				float(self.laf)
			except:
				self.laf = 0
			self.resultPage = self.init_resultPage()
			self.layout.addWidget(self.resultPage)
			self.layout.setCurrentWidget(self.resultPage)
		except:
			error_message()
			self.clearAll()

	def clearAll(self):
		self.entryAge.setDate(QDate.currentDate())
		# Probabilmente c'è un modo più intelligente per farlo...
		self.entrySexM.setAutoExclusive(False);
		self.entrySexM.setChecked(False);
		self.entrySexM.setAutoExclusive(True);
		self.entrySexF.setAutoExclusive(False);
		self.entrySexF.setChecked(False);
		self.entrySexF.setAutoExclusive(True);

		self.entryHeight.clear()
		self.entryWeight.clear()
		self.entryLaf.clear()

	def goBack(self):
		self.layout.setCurrentWidget(self.calcPage)
		self.clearAll()

app = QApplication(sys.argv)
geeno = MainWindow()
geeno.show()
app.exec_()

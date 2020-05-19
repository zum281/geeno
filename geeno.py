import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtGui



def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

stylesheet = open(resource_path("style.qss")).read()

def error_message():
	msg = QMessageBox()
	msg.setGeometry(300, 100, 300, 250)
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
		return "Underweight"
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

def getDesiredWeight(bmi, height):
	return round(bmi * ((height/100) ** 2), 1)

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
		self.layout.addWidget(self.calcPage)

		self.layout.setCurrentWidget(self.calcPage)

		widget = QWidget()
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)

	def init_calcPage(self):
		self.setGeometry(300, 100, 300, 250)
		layout = QGridLayout()
		lblWelcome = QLabel("GEENO Calculator", objectName='lblWelcome')
		layout.addWidget(lblWelcome, 0, 0, 1, 3, Qt.AlignCenter)

		# date of birth
		lblAge = QLabel("Date of birth: ")
		layout.addWidget(lblAge, 1, 0)
		self.entryAge = QDateEdit()
		self.entryAge.setDate(QDate.currentDate())
		self.entryAge.setCalendarPopup(True)
		self.entryAge.setDisplayFormat("dd/MM/yyyy")
		layout.addWidget(self.entryAge, 2, 0)

		# height
		lblHeight = QLabel("Heigth (cm): ")
		layout.addWidget(lblHeight, 3, 0)
		self.entryHeight = QLineEdit()
		self.entryHeight.setValidator(QtGui.QIntValidator())
		self.entryHeight.setMaxLength(3)
		layout.addWidget(self.entryHeight, 4, 0)


		# weight
		lblWeight = QLabel("Weight (kg): ")
		layout.addWidget(lblWeight, 5, 0)
		self.entryWeight = QLineEdit()
		self.entryWeight.setValidator(QtGui.QDoubleValidator())
		layout.addWidget(self.entryWeight, 6, 0)

		# sex
		self.btnGroup = QButtonGroup()
		lblSex = QLabel("Sex: ")
		layout.addWidget(lblSex, 7, 0)
		self.entrySexM = QRadioButton("M")
		layout.addWidget(self.entrySexM, 8, 0)
		self.entrySexF = QRadioButton("F")
		layout.addWidget(self.entrySexF, 9, 0)
		self.btnGroup.addButton(self.entrySexM)
		self.btnGroup.addButton(self.entrySexF)

		# laf
		lblLaf = QLabel("LAF: ")
		layout.addWidget(lblLaf, 10, 0)
		self.entryLaf = QLineEdit()
		self.entryLaf.setValidator(QtGui.QDoubleValidator())
		layout.addWidget(self.entryLaf, 11, 0)


		self.clearAllBtn = QPushButton("Clear")
		self.clearAllBtn.clicked.connect(lambda: self.clearAll())
		layout.addWidget(self.clearAllBtn, 12, 0)
		self.goToResults = QPushButton("Results")
		self.goToResults.clicked.connect(lambda: self.getInput())
		self.goToResults.setAutoDefault(True)
		layout.addWidget(self.goToResults, 13, 0)

		calcPage = QWidget()
		calcPage.setLayout(layout)

		return calcPage

	def init_resultPage(self):
		layout = QGridLayout()

		layout.addWidget(QLabel("<i>Patient Info</i>", objectName='patientInfo'), 0, 0)
		layout.addWidget(QLabel("<i>Results</i>", objectName='results'), 0, 1)
		lblBirthDay = QLabel("<b>Birthday:</b> " + self.birthday.toString('d/MM/yyyy'))
		layout.addWidget(lblBirthDay, 1, 0)
		lblAge = QLabel("<b>Age:</b> "+str(self.age))
		layout.addWidget(lblAge, 2, 0)
		lblHeight = QLabel("<b>Height:</b> "+self.height)
		layout.addWidget(lblHeight, 3, 0)
		lblWeight = QLabel("<b>Weight:</b> "+self.weight)
		layout.addWidget(lblWeight, 4, 0)
		lblSex = QLabel("<b>Sex:</b> "+self.sex)
		layout.addWidget(lblSex, 5, 0)
		lblLaf = QLabel("<b>LAF:</b> " + str(self.laf))
		layout.addWidget(lblLaf, 6, 0)
		# BMR
		self.bmr = getBmr(int(self.age), self.sex,  float(self.weight), int(self.height))
		lblBmr = QLabel("<b>BMR:</b> "+ str(self.bmr))
		layout.addWidget(lblBmr, 1, 1)
		# BMI
		bmi = getBmi(float(self.weight), int(self.height))
		lblBmi = QLabel("<b>BMI:</b> " + str(bmi))
		layout.addWidget(lblBmi, 2, 1)
		lblBmiRange = QLabel("<b>BMI range:</b>\n"+str(getBmiRange(bmi)))
		layout.addWidget(lblBmiRange, 3, 1)

		# TEE (Total Energy Expenditure (?))
		self.tee = round(self.bmr*float(self.laf), 2)
		layout.addWidget(QLabel("<b>TEE:</b> "+str(self.tee)), 4, 1 )
	#	layout.addWidget(QLabel("Thank you for using geeno!"), 7,0)

		self.anotherBtn = QPushButton("New")
		self.anotherBtn.clicked.connect(lambda: self.goBack())
		layout.addWidget(self.anotherBtn, 8, 0)

		self.goToNextBtn = QPushButton("Next Step")
		self.goToNextBtn.clicked.connect(lambda: self.goToFirstObjective())
		layout.addWidget(self.goToNextBtn, 8, 1)

		self.goBackBtn = QPushButton("Go Back")
		self.goBackBtn.clicked.connect(lambda: self.layout.setCurrentWidget(self.calcPage))
		layout.addWidget(self.goBackBtn, 9, 0)

		exitBtn = QPushButton("Quit")
		exitBtn.clicked.connect(self.close)
		layout.addWidget(exitBtn, 9, 1)

		resultPage = QWidget()
		resultPage.setLayout(layout)

		return resultPage

	def init_objectivePage(self):
		layout = QGridLayout()
		self.lafInfoLbl = QLabel("Using LAF value " + str(self.laf))
		layout.addWidget(self.lafInfoLbl, 0, 0)
		layout.addWidget(QLabel("Enter new LAF value if needed:"), 1, 0)

		self.entryLaf = QLineEdit()
		self.entryLaf.setValidator(QtGui.QDoubleValidator())
		layout.addWidget(self.entryLaf, 2, 0)


		layout.addWidget(QLabel("Desired BMI "), 3, 0)
		self.bmiEntry = QLineEdit()
		self.bmiEntry.setValidator(QtGui.QDoubleValidator())
		self.bmiEntry.setMaxLength(4)
		layout.addWidget(self.bmiEntry, 4, 0)

		layout.addWidget(QLabel("Desired time range (months)"), 5, 0)
		self.timeRangeEntry = QLineEdit()
		self.timeRangeEntry.setValidator(QtGui.QIntValidator())
		self.timeRangeEntry.setMaxLength(2)
		layout.addWidget(self.timeRangeEntry, 6, 0)

		self.submitBtn = QPushButton("Submit")
		self.submitBtn.clicked.connect(lambda: self.calcCalories())
		layout.addWidget(self.submitBtn, 7, 0, 1, 3)

		self.desiredWeightLbl = QLabel("")
		layout.addWidget(QLabel("Desired Weight:"), 8, 0)
		layout.addWidget(self.desiredWeightLbl, 9, 0)

		self.firstObjectiveLbl = QLabel("")
		layout.addWidget(QLabel("First objective:"), 10, 0)
		layout.addWidget(self.firstObjectiveLbl, 11, 0)

		self.goToStartBtn = QPushButton("Start Again")
		self.goToStartBtn.clicked.connect(lambda: self.goBack())
		layout.addWidget(self.goToStartBtn, 12, 0)

		exitBtn = QPushButton("Quit")
		exitBtn.clicked.connect(self.close)
		layout.addWidget(exitBtn, 13, 0)

		objectivePage = QWidget()
		objectivePage.setLayout(layout)

		return objectivePage

	def calcCalories(self):
		oldLaf = float(self.laf)
		try:
			try:
				self.laf = float(self.entryLaf.text())
			except:
				self.laf = oldLaf

			self.lafInfoLbl.setText("Using LAF value " + str(self.laf))
			self.tee = round(self.bmr*float(self.laf), 2)
			#self.objectiveLayout.addWidget(QLabel("TEE = " +str(self.tee)), 15, 0)
			desiredBmi = self.bmiEntry.text()
			desiredWeight = getDesiredWeight(float(desiredBmi), int(self.height))
			months = self.timeRangeEntry.text()
			desiredDays = int(months) * 30 # to be fixed
			self.desiredWeightLbl.setText(str(desiredWeight))
			# RESULT = TEE - la roba sopra
			# (PESO ATTUALE - PESO IDEALE) * 7000 / NUMERO GIORNI (In desired time range)
			result = round(float(self.tee) - (((float(self.weight) - desiredWeight) * 7000) / desiredDays), 1)
			self.firstObjectiveLbl.setText(str(result))

		except:
			error_message()
			self.bmiEntry.clear()
			self.timeRangeEntry.clear()

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
			# TEST VALUES!!!
			#self.height = str(187)
			#self.weight = str(76)
			#self.sex = 'M'
			#self.laf = 1.5
			#self.resultPage = self.init_resultPage()
			#self.layout.addWidget(self.resultPage)
			#self.layout.setCurrentWidget(self.resultPage)

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

	def goToFirstObjective(self):
		self.objectivePage = self.init_objectivePage()
		self.layout.addWidget(self.objectivePage)
		self.layout.setCurrentWidget(self.objectivePage)


app = QApplication(sys.argv)
app.setStyleSheet(stylesheet)
geeno = MainWindow()
geeno.show()
app.exec_()

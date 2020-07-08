import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtGui


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
        age = age - 1
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
    return round(bmi * ((height / 100) ** 2), 1)


def getDesiredBmi(weight, height):
    return round(weight * ((100 / height) ** 2), 1)

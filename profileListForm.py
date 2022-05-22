import sys
import os
from unittest import skip
import cv2
import re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from User import User
from userEditForm import UserEditDialog
from HistoryRecord import HistoryRecord
class ProfileListForm(QDialog):
    def __init__(self):
        super(ProfileListForm,self).__init__()
        loadUi("ui/userListUI.ui",self)
        self.Count = 0
        self.formStySheet()
        self.listHistory = []
        self._new_window = None
        self.editUserButton.clicked.connect(self.editUserButtonExec)
        self.nextButton.clicked.connect(self.nextButtonExec)
        self.preButton.clicked.connect(self.preButtonExec)
        self.fpath = os.listdir("db")
        self.num.setText(f"{self.Count+1}/{len(self.fpath)}")
        for i in self.fpath:
            with open(f"db/{i}","r") as f:
                tmp = f.readlines()
                tmp1 = User(tmp[0][0:len(tmp[0])-1],tmp[1][0:len(tmp[1])-1],tmp[2][0:len(tmp[2])-1],tmp[3])
                self.listHistory.append(tmp1)
        fpath1 = os.listdir("history")
        for path in range(len(fpath1)-1,-1,-1):
            with open(f"history/{fpath1[path]}","r") as file:
                A = file.readlines()
                for tmp in range(len(A)-1,-1,-1):
                    tmp1 = HistoryRecord(A[tmp])
                    try:
                        self.listHistory[int(tmp1.id)-1].loginHistory.append(tmp1)
                    except IndexError:
                        skip
        self.changeData()

    def scrollChange(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        for i in self.listHistory[self.Count].loginHistory:
            myform.addRow(QLabel(i.strOutput()))
        mygroupbox.setLayout(myform)
        self.historyDisplay.setWidget(mygroupbox)
    @pyqtSlot()
    def editUserButtonExec(self):
        self._new_window = UserEditDialog(self.listHistory[self.Count])
        self._new_window.show()


    @pyqtSlot()
    def nextButtonExec(self):
        if self.Count == len(self.fpath)-1:
            self.Count = 0
        else:
            self.Count += 1
        self.changeData()


    @pyqtSlot()
    def preButtonExec(self):
        if self.Count == 0:
            self.Count = len(self.fpath)-1
        else:
            self.Count -= 1
        self.changeData()

    def changeData(self):
        self.num.setText(f"{self.Count+1}/{len(self.fpath)}")
        self.id.setText(f"Mã số người dùng: {self.listHistory[self.Count].id}")
        self.name.setText(f"Họ và tên: {self.listHistory[self.Count].name}")
        self.sex.setText(f"Giới tính: {self.listHistory[self.Count].sex}")
        self.dob.setText(f"Ngày sinh: {self.listHistory[self.Count].dob}")
        self.image.setPixmap(QPixmap(f"profileImage/{self.listHistory[self.Count].id}.jpg").scaled(280, 280, Qt.KeepAspectRatio))
        self.scrollChange()

        
    def formStySheet(self):
        with open("stylesheet/longButton.txt","r") as f:
            self.editUserButton.setStyleSheet(f.read())
        with open("stylesheet/nextButton.txt","r") as f:
            self.nextButton.setStyleSheet(f.read())
        with open("stylesheet/preButton.txt","r") as f:
            self.preButton.setStyleSheet(f.read())
        with open("stylesheet/roundRectangleLabel.txt","r") as f:
            self.label.setStyleSheet(f.read())
        with open("stylesheet/scrollArea.txt") as f:
            self.historyDisplay.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    startUi = ProfileListForm()
    startUi.show()
    sys.exit(app.exec_())
import sys
import os
import cv2
import re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from User import User
from userEditForm import UserEditDialog
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
        self.id.setText(f"Mã số người dùng: {self.listHistory[self.Count].id}")
        self.name.setText(f"Họ và tên: {self.listHistory[self.Count].name}")
        self.sex.setText(f"Giới tính: {self.listHistory[self.Count].sex}")
        self.dob.setText(f"Ngày sinh: {self.listHistory[self.Count].dob}")
        self.image.setPixmap(QPixmap(f"profileImage/{self.listHistory[self.Count].id}.jpg").scaled(280, 280, Qt.KeepAspectRatio))


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

        
    def formStySheet(self):
        with open("stylesheet/longButton.txt","r") as f:
            self.editUserButton.setStyleSheet(f.read())
        with open("stylesheet/nextButton.txt","r") as f:
            self.nextButton.setStyleSheet(f.read())
        with open("stylesheet/preButton.txt","r") as f:
            self.preButton.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    startUi = ProfileListForm()
    startUi.show()
    sys.exit(app.exec_())
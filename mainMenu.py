
import sys
import os
from User import User
from tkinter import Image
from unittest import result
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from imageThread import ImageThread
from PIL import ImageQt
from historyForm import HistoryDialog
from datetime import datetime as dt
from userAddform import UserAddDialog
from userEditForm import UserEditDialog
from profileListForm import ProfileListForm
import numpy as np
import cv2
import face_recognition
import glob
from threading import Event

from userEditForm import UserEditDialog
class MenuDialog(QDialog):
    def __init__(self):
        super(MenuDialog, self).__init__()
        loadUi("ui/menuUI1.ui",self)
        self.menuStyleSheet()
        self.startFuncButton.clicked.connect(self.startFuncButtonExec)
        self.editButton.clicked.connect(self.editUserButtonExec)
        self.loginButton.clicked.connect(self.loginButtonExec)
        self.historyButton.clicked.connect(self.historyButtonExec)
        self.profileButton.clicked.connect(self.profileButtonExec)
        self.loginButton.setEnabled(False)
        self.editButton.setVisible(False)
        self.imageThread = ImageThread()
        self.imageScreenState = False
        self.profileImage = os.listdir("profileImage")
        self._new_window = None

    
    
    def imageUpdateSlot(self, image):
        self.imageScreen.setPixmap(QPixmap.fromImage(image))


    def imageClearSlot(self,image):
        self.imageScreen.setPixmap(QPixmap("image/imageScreen_clear.png"))
    def cancelFeed(self):
        self.imageThread.stop()
    
    
    #StyleSheet
    def menuStyleSheet(self):
        with open("stylesheet/button.txt","r") as f:
            A = f.read()
            self.profileButton.setStyleSheet(A)
            self.historyButton.setStyleSheet(A)
            self.loginButton.setStyleSheet(A)
            self.editButton.setStyleSheet(A)
        with open("stylesheet/longButton.txt","r") as f:
            self.startFuncButton.setStyleSheet(f.read())
        with open("stylesheet/outline.txt","r") as f:
            A = f.read()
            self.outLine.setStyleSheet(A)
            self.outLine2.setStyleSheet(A)
            self.userImage.setStyleSheet(A)
            self.imageScreen.setStyleSheet(A)
        with open("stylesheet/scrollArea.txt","r") as f:
            self.historyDisplay.setStyleSheet(f.read())
        with open("stylesheet/imageScreen.txt","r") as f:
            self.imageScreen.setStyleSheet(f.read())
        with open("stylesheet/mask.txt","r") as f:
            self.mask.setStyleSheet(f.read())
    
    
    @pyqtSlot()
    def editUserButtonExec(self):
        if(self.imageThread.classFoundName == "None" or self.imageThread.classFoundName == "") and self.imageThread.faceCheck == True:
            self._new_window = UserAddDialog(os.listdir("db")[len(os.listdir("db"))-1])
            self._new_window.show()
        elif(self.imageThread.classFoundName != "None"):
            self._new_window = UserEditDialog(self.user)
            self._new_window.show()


    @pyqtSlot()
    def startFuncButtonExec(self):
        if self.imageScreenState:
            self.imageThread.stop()
            self.editButton.setVisible(False)
            self.imageThread.imageUpdate.connect(self.imageClearSlot)
            self.startFuncButton.setText("Bật nguồn camera")
            self.loginButton.setEnabled(False)
            self.imageScreenState = False
        else:
            self.imageThread.start()
            self.imageThread.imageUpdate.connect(self.imageUpdateSlot)
            self.startFuncButton.setText("Tắt nguồn camera")
            self.loginButton.setEnabled(True)
            self.imageScreenState = True
    @pyqtSlot()
    def loginButtonExec(self):
        self.imageThread.classFoundName = "None"
        self.imageThread.pressCheck = True
        Event().wait(7)
        if(self.imageThread.classFoundName != "None" and self.imageThread.classFoundName != ""):
            with open(f"db/{self.imageThread.classFoundName}.txt","r") as file:
                A = file.readlines()
                tmp = A[1][0:len(A[1])-1]
                self.user = User(A[0][0:len(A[0])-1],tmp,A[2][0:len(A[2])-1],A[3])
                self.userImage.setPixmap(QPixmap(f"profileImage/{self.imageThread.classFoundName}.jpg").scaled(130, 110, Qt.KeepAspectRatio))
                self.userName.setText(f'Họ và tên: {tmp}')
                self.userSex.setText(f'Giới tính: {A[2][0:len(A[2])-1]}')
                self.userDob.setText(f'Ngày sinh: {A[3]}')
                self.editButton.setText("Chỉnh sửa")
                self.editButton.setVisible(True)
                self.findUserHistory(A[0][0:len(A[0])-1])
                dateStr = dt.now().strftime("%Y_%m.txt")
                with open(f"history/{dateStr}","a") as saveFile:
                    dateStr = dt.now().strftime("%Y/%m/%d %H : %M : %S")
                    saveFile.write(f"\n{self.user.id}; {dateStr}; {self.user.name};")
                self.editButton.setEnabled(True)
        else:
            self.userName.setText('Họ và tên:')
            self.userSex.setText('Giới tính:')
            self.userDob.setText('Ngày sinh:')
            self.historyDisplay.setWidget(QGroupBox())
            if(self.imageThread.faceCheck == True):
                self.editButton.setText("Thêm mới")
                self.editButton.setVisible(True)
                self.editButton.setEnabled(True)
            else:
                self.editButton.setVisible(False)
            self.userImage.setPixmap(QPixmap("image/cleanAva.png"))
    

    def findUserHistory(self,userNameFind):
        Count = 0
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        listHistory = []
        fpath = os.listdir("history")
        for path in range(len(fpath)-1,-1,-1):
            with open(f"history/{fpath[path]}","r") as file:
                A = file.readlines()
                for tmp in range(len(A)-1,-1,-1):
                    tmp1 = A[tmp].split(';')
                    if(tmp1[0] == userNameFind):
                        myform.addRow(QLabel(tmp1[1]))
                        Count += 1
                    if Count >= 4:
                        mygroupbox.setLayout(myform)
                        self.historyDisplay.setWidget(mygroupbox)
                        return
            if Count >= 4:
                mygroupbox.setLayout(myform)
                self.historyDisplay.setWidget(mygroupbox)
                return
        mygroupbox.setLayout(myform)
        self.historyDisplay.setWidget(mygroupbox)
    
    
    @pyqtSlot()
    def historyButtonExec(self):
        self._new_window = HistoryDialog()
        self._new_window.show()
    
    
    @pyqtSlot()
    def profileButtonExec(self):
        self._new_window = ProfileListForm()
        self._new_window.show()

                        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    startUi = MenuDialog()
    startUi.show()
    sys.exit(app.exec_())
        
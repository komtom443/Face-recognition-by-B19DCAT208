  
from email.mime import image
import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainMenu import MenuDialog
class StartDialog(QDialog):
    imageList = []
    def __init__(self):
        self.Count = 0
        super(StartDialog,self).__init__()
        loadUi("ui/startUI.ui",self)
        self._new_window = None
        self.Videocapture_ = None
        self.startButton.clicked.connect(self.startButtonRun)
        for i in os.listdir("memberProfile"):
            self.imageList.append(f"memberProfile/{i}")
        self.menuStyleSheet()

        
    def refreshAll(self):
        self.Videocapture_ = "0"
    def menuStyleSheet(self):
        print(self.imageList[0])
        self.label.setStyleSheet("QLabel"
                                "{"
                                f"border-image: url({self.imageList[0]}) 0 0 0 0 stretch stretch;"
                                "}"
                                )
        with open("stylesheet/longButton.txt","r") as f:
            self.startButton.setStyleSheet(f.read())
        with open("stylesheet/nextButton.txt","r") as f:
            self.nextButton.setStyleSheet(f.read())
        with open("stylesheet/preButton.txt","r") as f:
            self.preButton.setStyleSheet(f.read())
    @pyqtSlot()
    def startButtonRun(self):
        print("Start")
        self.refreshAll()
        print(self.Videocapture_)
        startUi.hide()
        startUi.outputWindow()
    def outputWindow(self):
        self._new_window = MenuDialog()
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
        self.label.setStyleSheet("QLabel"
                                "{"
                                f"border-image: url({self.imageList[self.Count]}) 0 0 0 0 stretch stretch;"
                                "}"
                                )
if __name__ == "__main__":
    app = QApplication(sys.argv)
    startUi = StartDialog()
    startUi.show()
    sys.exit(app.exec_())

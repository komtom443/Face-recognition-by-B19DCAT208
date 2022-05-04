import sys
import os
import re
from datetime import datetime as dt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from User import User
class HistoryRecord:
    def __init__(self,A):
        self.inputStr = str
        tmp1 = A.split(';')
        self.id = tmp1[0]
        try:
            with open(f"db/{self.id}.txt","r") as f:
                tmp = f.readlines()[1]
                self.name = tmp[0:len(tmp)-1]
        except FileNotFoundError:
            self.name = f"{tmp1[2]}  (Profile đã xóa)"
        tmp = dt.strptime(tmp1[1]," %Y/%m/%d %H : %M : %S")
        self.time = [dt.strftime(tmp,r"%d/%m/%Y"),dt.strftime(tmp,"%H : %M : %S")]
    def strOutput(self):
        return f"ID người dùng: {self.id}\nHọ và Tên: {self.name}\nThời gian: {self.time[0]}\t{self.time[1]}"
    def searchStr(self):
        tmp = f"id {self.id} {self.name.lower()} {self.time[0]} {self.time[1]}".lower()
        return tmp


class HistoryDialog(QDialog):
    upCheck = False
    def __init__(self):
        super(HistoryDialog,self).__init__()
        loadUi("ui/historyUi.ui",self)
        self.listHistory = []
        self.searchButton.clicked.connect(self.searchButtonExec)
        self.sortButton.clicked.connect(self.sortButtonExec)
        self.excelButton.clicked.connect(self.excelButtonExec)
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        fpath = os.listdir("history")
        self.historyStyleSheet()
        for path in range(len(fpath)-1,-1,-1):
            with open(f"history/{fpath[path]}","r") as file:
                A = file.readlines()
                for tmp in range(len(A)-1,-1,-1):
                    tmp1 = HistoryRecord(A[tmp])
                    self.listHistory.append(tmp1)
                    myform.addRow(QLabel(tmp1.strOutput()))
        self.exportList = self.listHistory
        mygroupbox.setLayout(myform)
        self.historyDisplay.setWidget(mygroupbox)
    
    
    def historyStyleSheet(self):
        with open("stylesheet/searchButton.txt") as f:
            self.searchButton.setStyleSheet(f.read())
        with open("stylesheet/scrollArea.txt") as f:
            self.historyDisplay.setStyleSheet(f.read())
        with open("stylesheet/plainText.txt") as f:
            self.textEdit.setStyleSheet(f.read())
        with open("stylesheet/excelButton.txt") as f:
            self.excelButton.setStyleSheet(f.read())
        with open("stylesheet/outline.txt") as f:
            self.label.setStyleSheet(f.read())
        with open("stylesheet/sortDownButton.txt") as f:
            self.sortButton.setStyleSheet(f.read())
    
    
    @pyqtSlot()
    def searchButtonExec(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        Count = 0
        tmp = self.textEdit.toPlainText()
        tmp.lower()
        self.exportList = []
        tmp = self.no_accent_vietnamese(tmp).lower()
        print(tmp)
        for i in self.listHistory:
            if i.searchStr().find(tmp) != -1:
                myform.addRow(QLabel(i.strOutput()))
                self.exportList.append(i)
                Count += 1
        mygroupbox.setLayout(myform)
        self.historyDisplay.setWidget(mygroupbox)
        self.textEdit.setText("")
        if tmp != "":
            self.status.setText(f"We Found {Count}/{len(self.listHistory)}")
        else:
            self.status.setText("")
    
    
    @pyqtSlot()
    def sortButtonExec(self):
        if self.upCheck == False:
            self.upCheck = True
            with open("stylesheet/sortUpButton.txt") as f:
                self.sortButton.setStyleSheet(f.read())
        else:
            self.upCheck = False
            with open("stylesheet/sortDownButton.txt") as f:
                self.sortButton.setStyleSheet(f.read())
        self.exportList.reverse()
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        for i in self.exportList:
            myform.addRow(QLabel(i.strOutput()))
        mygroupbox.setLayout(myform)
        self.historyDisplay.setWidget(mygroupbox)


    @pyqtSlot()
    def excelButtonExec(self):
        tmp = len(os.listdir("exportFile"))
        if tmp == 0:
            with open("exportFile/export.csv","w") as f:
                for i in self.exportList:
                    f.write(f"{i.id},\"{i.name}\",{i.time[0]},{i.time[1]}\n")
        else:
            with open(f"exportFile/export{tmp}.csv","w") as f:
                for i in self.exportList:
                    f.write(f"{i.id},\"{i.name}\",{i.time[0]},{i.time[1]}\n")
        self.status.setText(f"File is export successfully")
        

    def no_accent_vietnamese(self,s):
        s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
        s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
        s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
        s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
        s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
        s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
        s = re.sub('[íìỉĩị]', 'i', s)
        s = re.sub('[ÍÌỈĨỊ]', 'I', s)
        s = re.sub('[úùủũụưứừửữự]', 'u', s)
        s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
        s = re.sub('[ýỳỷỹỵ]', 'y', s)
        s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
        s = re.sub('đ', 'd', s)
        s = re.sub('Đ', 'D', s)
        return s

if __name__ == "__main__":
    app = QApplication(sys.argv)
    startUi = HistoryDialog()
    startUi.show()
    sys.exit(app.exec_())
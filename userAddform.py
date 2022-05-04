import re
import sys
import os
import cv2
from datetime import datetime as dt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from User import User
class UserAddDialog(QDialog):
    def __init__(self,id):
        super(UserAddDialog,self).__init__()
        loadUi("ui/userAddUi.ui",self)
        self.userImage.setPixmap(QPixmap("image/tmp.jpg").scaled(280, 280, Qt.KeepAspectRatio))
        self.saveButton.clicked.connect(self.saveButtonExec)
        self.img = cv2.imread("image/tmp.jpg")
        with open(f"db/{id}","r") as f:
            self.id = int(f.readline())+1
        with open("stylesheet/saveButton.txt","r") as f:
            self.saveButton.setStyleSheet(f.read())
    @pyqtSlot()
    def saveButtonExec(self):
        if self.nameValue.toPlainText() == "" or self.yearDobValue.toPlainText() == "" or self.monthDobValue.toPlainText() == "" or self.dayDobValue.toPlainText() == "":
            self.status.setText("Vui lòng điền hết ô trống !")
            return
        try:
            date = dt.strptime(f"{self.dayDobValue.toPlainText()}/{self.monthDobValue.toPlainText()}/{self.yearDobValue.toPlainText()}",'%d/%m/%Y')
            sex = ""
            if self.male.isChecked():
                sex = "Male"
            else:
                sex = "Female"
            self.user = User(self.id,self.nameValue.toPlainText(),sex,date.strftime("%d/%m/%Y"))
        except ValueError:
            self.status.setText("Ngày tháng năm không hợp lệ!")
            return
        with open(f"db/{self.user.id}.txt","w") as f:
            f.write(f"{str(self.user.id)}\n{self.no_accent_vietnamese(self.user.name)}\n{self.user.sex}\n{self.user.dob}")
            cv2.imwrite(f"profileImage/{self.user.id}.jpg",self.img)
            self.status.setText("Lưu thành công")


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
    startUi = UserAddDialog()
    startUi.show()
    sys.exit(app.exec_())
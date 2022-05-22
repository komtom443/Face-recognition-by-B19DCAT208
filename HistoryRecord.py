from datetime import datetime as dt
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
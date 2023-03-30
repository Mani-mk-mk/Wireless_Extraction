from PyQt5 import QtWidgets, QtSql
# from PyQt5.QtWidgets import QLineEdit 
from login import Ui_MainWindow
import sys

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(App, self).__init__(parent = parent)
        self.setupUi(self)
        self.openDB()
        self.pushButton.clicked.connect(self.checkUser)

    def openDB(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data.sqlite")
        if not self.db.open():
            print("Error")
        
        self.query = QtSql.QSqlQuery()

    def checkUser(self):
        username1 = self.username.text()
        password1 = self.password.text()
        print(username1, password1)
        # self.query.exec_("select * from userdata where username = '%s' and password = '%s';" %(username1, password1))
        # self.query.first()
        # if self.query.value("username") != None and self.query.value("password") != None:
        #     print("Login Successful!")
        # else:
        #     print("Login Failed!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())

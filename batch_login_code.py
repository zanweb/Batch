from batch_login import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

# from main_window_code import *


class LoginDialog(QtWidgets.QWidget, Ui_Dialog_login):

    def __init__(self):
        super(LoginDialog, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_init)
        self.pass_info = []
        self.lineEdit.setFocus()
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.main_w = MainWindow()

    def login_info(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "Login OK",
                                        "You will login the Batching...",  # + str(self.pass_info),
                                        QMessageBox.Ok)
        return reply

    def login_init(self):
        self.pass_info = []
        self.pass_info.append(self.comboBox.currentText())
        if self.lineEdit_2.text() == '' or self.lineEdit.text() == '':
            QMessageBox.information(self,  # 使用infomation信息框
                                    "Login",
                                    "Please fill the Username and Password...",  # + str(self.pass_info),
                                    QMessageBox.Ok)
            self.lineEdit.setFocus()
        else:
            self.pass_info.append(self.lineEdit.text())
            self.pass_info.append(self.lineEdit_2.text())
            # self.login_info()

            # self.main_w.show()
            self.hide()

        # pass

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    login_show = LoginDialog()
    login_show.show()
    sys.exit(app.exec_())
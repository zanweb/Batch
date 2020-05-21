#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2019/12/1 20:30
# @Author   :   ZANWEB
# @File     :   FrameDataCenterLogin_code.py in Batch
# @IDE      :   PyCharm

from configparser import ConfigParser

from PyQt5.QtWidgets import QMessageBox, QDialog
from pymssql import connect

from FrameDataCenterLogin import Ui_Dialog
from FrameDataCenter_code import *


class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_set()
        self.user_info = {'server': '', 'database': '', 'account': '', 'password': ''}

    def ui_set(self):
        self.combo_box_factory.addItems(['TianJin', 'XiAn', 'ShangHai', 'Test', 'Test2'])
        self.push_button_ok.clicked.connect(self.login_function)

    def login_function(self):
        factory = self.combo_box_factory.currentText()
        account = self.line_edit_account.text()
        password = self.line_edit_password.text()

        if (factory == '') or (account == '') or (password == ''):
            reply = QMessageBox.warning(self, '警告', '工厂/账号/密码不能为空,请输入!')
            return
        # 查询数据库

        result = self.check_user(factory, account, password)
        if result[0] > 0:
            main_window.user_info = self.user_info
            main_window.ui_set()
            main_window.show()

            self.close()
        else:
            reply = QMessageBox.warning(self, '警告', '工厂/账号/密码错误或请检查网络,请重新输入!')

    def check_user(self, factory, account, password):
        cf = ConfigParser()
        cf.read('config.ini')
        server = cf.get(factory, 'server')
        database = cf.get(factory, 'database')
        try:
            cnn = connect(host=server, user=account, password=password, database=database, as_dict=True)
            cnn.close()
            self.user_info = {'server': server, 'database': database, 'account': account, 'password': password}
            return 1, self.user_info
        except Exception as e:
            print(e)
            return 0, self.user_info


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    main_window = UiMain()
    window.show()
    sys.exit(app.exec())

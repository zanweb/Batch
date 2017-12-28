# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test.ui'
#
# Created: Sun Apr  2 21:46:12 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Test(object):
    def setupUi(self, Test):
        Test.setObjectName("Test")
        Test.resize(852, 714)
        Test.setFixedSize(852, 714)
        self.lineEdit = QtWidgets.QLineEdit(Test)
        self.lineEdit.setGeometry(QtCore.QRect(150, 20, 200, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget = QtWidgets.QListWidget(Test)
        self.listWidget.setGeometry(QtCore.QRect(0, 140, 420, 421))
        self.listWidget.setObjectName("listWidget")
        self.toolButton = QtWidgets.QToolButton(Test, clicked=lambda: self._resize(Test))
        self.toolButton.setGeometry(QtCore.QRect(0, 20, 41, 41))
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(Test)
        QtCore.QMetaObject.connectSlotsByName(Test)

    def retranslateUi(self, Test):
        _translate = QtCore.QCoreApplication.translate
        Test.setWindowTitle(_translate("Test", "Test"))
        self.toolButton.setText(_translate("Test", "<"))

    def _resize(self, Test):
        Test.resize(420, 714)  # 420, 714
        Test.setFixedSize(420, 714)
        self.listWidget.clear()  # 清空list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Test()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
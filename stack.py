# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stack.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form_report_stack_total(object):
    def setupUi(self, form_report_stack_total):
        form_report_stack_total.setObjectName("form_report_stack_total")
        form_report_stack_total.resize(600, 300)
        self.tableWidget = QtWidgets.QTableWidget(form_report_stack_total)
        self.tableWidget.setGeometry(QtCore.QRect(10, 0, 561, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(form_report_stack_total)
        QtCore.QMetaObject.connectSlotsByName(form_report_stack_total)

    def retranslateUi(self, form_report_stack_total):
        _translate = QtCore.QCoreApplication.translate
        form_report_stack_total.setWindowTitle(_translate("form_report_stack_total", "stack information"))


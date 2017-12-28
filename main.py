# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile_F = QtWidgets.QMenu(self.menubar)
        self.menuFile_F.setObjectName("menuFile_F")
        self.menuReport_Alt_R = QtWidgets.QMenu(self.menubar)
        self.menuReport_Alt_R.setObjectName("menuReport_Alt_R")
        # MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.actionSelect_Orders_Alt_S = QtWidgets.QAction(MainWindow)
        self.actionSelect_Orders_Alt_S.setObjectName("actionSelect_Orders_Alt_S")
        self.actionBatching_Alt_B = QtWidgets.QAction(MainWindow)
        self.actionBatching_Alt_B.setObjectName("actionBatching_Alt_B")
        self.actionStack_Total_Alt_T = QtWidgets.QAction(MainWindow)
        self.actionStack_Total_Alt_T.setObjectName("actionStack_Total_Alt_T")
        self.actionExit_Alt_X = QtWidgets.QAction(MainWindow)
        self.actionExit_Alt_X.setObjectName("actionExit_Alt_X")
        self.menuFile_F.addAction(self.actionSelect_Orders_Alt_S)
        self.menuFile_F.addAction(self.actionBatching_Alt_B)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.actionExit_Alt_X)
        self.menuReport_Alt_R.addAction(self.actionStack_Total_Alt_T)
        self.menubar.addAction(self.menuFile_F.menuAction())
        self.menubar.addAction(self.menuReport_Alt_R.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile_F.setTitle(_translate("MainWindow", "File(Alt-F)"))
        self.menuReport_Alt_R.setTitle(_translate("MainWindow", "Report(Alt-R)"))
        self.actionSelect_Orders_Alt_S.setText(_translate("MainWindow", "Select Orders(Alt-S)"))
        self.actionBatching_Alt_B.setText(_translate("MainWindow", "Batching(Alt-B)"))
        self.actionStack_Total_Alt_T.setText(_translate("MainWindow", "Stack Total(Alt-T)"))
        self.actionExit_Alt_X.setText(_translate("MainWindow", "Exit(Alt-X)"))


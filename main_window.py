# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(444, 427)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_show_orders = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_show_orders.setGeometry(QtCore.QRect(30, 70, 141, 51))
        self.pushButton_show_orders.setMinimumSize(QtCore.QSize(131, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_show_orders.setFont(font)
        self.pushButton_show_orders.setMouseTracking(True)
        self.pushButton_show_orders.setAutoFillBackground(True)
        self.pushButton_show_orders.setObjectName("pushButton_show_orders")
        self.pushButton_batching = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_batching.setGeometry(QtCore.QRect(190, 70, 141, 51))
        self.pushButton_batching.setMinimumSize(QtCore.QSize(141, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_batching.setFont(font)
        self.pushButton_batching.setMouseTracking(True)
        self.pushButton_batching.setObjectName("pushButton_batching")
        self.pushButton_show_batch_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_show_batch_report.setGeometry(QtCore.QRect(20, 290, 181, 41))
        self.pushButton_show_batch_report.setMinimumSize(QtCore.QSize(161, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_show_batch_report.setFont(font)
        self.pushButton_show_batch_report.setObjectName("pushButton_show_batch_report")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_nc_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_nc_path.setGeometry(QtCore.QRect(120, 160, 301, 20))
        self.lineEdit_nc_path.setObjectName("lineEdit_nc_path")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 160, 71, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_browse_nc_path = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browse_nc_path.setGeometry(QtCore.QRect(130, 190, 91, 31))
        self.pushButton_browse_nc_path.setMouseTracking(True)
        self.pushButton_browse_nc_path.setObjectName("pushButton_browse_nc_path")
        self.pushButton_nc_deal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nc_deal.setGeometry(QtCore.QRect(250, 190, 101, 31))
        self.pushButton_nc_deal.setMouseTracking(True)
        self.pushButton_nc_deal.setObjectName("pushButton_nc_deal")
        self.pushButton_stack_with_subparts = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stack_with_subparts.setGeometry(QtCore.QRect(20, 340, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_stack_with_subparts.setFont(font)
        self.pushButton_stack_with_subparts.setObjectName("pushButton_stack_with_subparts")
        self.pushButton_stiff_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stiff_view.setGeometry(QtCore.QRect(20, 490, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_stiff_view.setFont(font)
        self.pushButton_stiff_view.setObjectName("pushButton_stiff_view")
        self.pushButton_burn_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_burn_view.setGeometry(QtCore.QRect(20, 640, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_burn_view.setFont(font)
        self.pushButton_burn_view.setObjectName("pushButton_burn_view")
        self.pushButton_clip_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clip_view.setGeometry(QtCore.QRect(20, 540, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_clip_view.setFont(font)
        self.pushButton_clip_view.setObjectName("pushButton_clip_view")
        self.pushButton_plate_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plate_view.setGeometry(QtCore.QRect(20, 590, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_plate_view.setFont(font)
        self.pushButton_plate_view.setObjectName("pushButton_plate_view")
        self.pushButton_web_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_web_view.setGeometry(QtCore.QRect(20, 440, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_web_view.setFont(font)
        self.pushButton_web_view.setObjectName("pushButton_web_view")
        self.pushButton_flange_view = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_flange_view.setGeometry(QtCore.QRect(20, 390, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_flange_view.setFont(font)
        self.pushButton_flange_view.setObjectName("pushButton_flange_view")
        self.pushButton_flange_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_flange_report.setGeometry(QtCore.QRect(250, 390, 171, 41))
        self.pushButton_flange_report.setObjectName("pushButton_flange_report")
        self.pushButton_web_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_web_report.setGeometry(QtCore.QRect(250, 440, 171, 41))
        self.pushButton_web_report.setObjectName("pushButton_web_report")
        self.pushButton_stiff_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stiff_report.setGeometry(QtCore.QRect(250, 490, 171, 41))
        self.pushButton_stiff_report.setObjectName("pushButton_stiff_report")
        self.pushButton_clip_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clip_report.setGeometry(QtCore.QRect(250, 540, 171, 41))
        self.pushButton_clip_report.setObjectName("pushButton_clip_report")
        self.pushButton_plate_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plate_report.setGeometry(QtCore.QRect(250, 590, 171, 41))
        self.pushButton_plate_report.setObjectName("pushButton_plate_report")
        self.pushButton_burn_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_burn_report.setGeometry(QtCore.QRect(250, 640, 171, 41))
        self.pushButton_burn_report.setObjectName("pushButton_burn_report")
        self.pushButton_all_report = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_all_report.setGeometry(QtCore.QRect(250, 290, 171, 81))
        self.pushButton_all_report.setMouseTracking(True)
        self.pushButton_all_report.setObjectName("pushButton_all_report")
        self.lineEdit_Batch_the_Batch = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Batch_the_Batch.setGeometry(QtCore.QRect(160, 260, 261, 21))
        self.lineEdit_Batch_the_Batch.setObjectName("lineEdit_Batch_the_Batch")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 260, 101, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(160, 240, 261, 16))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 444, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile_F = QtWidgets.QMenu(self.menubar)
        self.menuFile_F.setObjectName("menuFile_F")
        self.menuReport_Alt_R = QtWidgets.QMenu(self.menubar)
        self.menuReport_Alt_R.setObjectName("menuReport_Alt_R")
        self.menuView_V = QtWidgets.QMenu(self.menubar)
        self.menuView_V.setObjectName("menuView_V")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setMinimumSize(QtCore.QSize(0, 22))
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionSelect_Orders_Alt_S = QtWidgets.QAction(MainWindow)
        self.actionSelect_Orders_Alt_S.setObjectName("actionSelect_Orders_Alt_S")
        self.actionBatching_Alt_B = QtWidgets.QAction(MainWindow)
        self.actionBatching_Alt_B.setObjectName("actionBatching_Alt_B")
        self.actionStack_Total_Alt_T = QtWidgets.QAction(MainWindow)
        self.actionStack_Total_Alt_T.setObjectName("actionStack_Total_Alt_T")
        self.actionExit_Alt_X = QtWidgets.QAction(MainWindow)
        self.actionExit_Alt_X.setObjectName("actionExit_Alt_X")
        self.actionShow_Batch_Report = QtWidgets.QAction(MainWindow)
        self.actionShow_Batch_Report.setObjectName("actionShow_Batch_Report")
        self.actionStacks_with_Subparts = QtWidgets.QAction(MainWindow)
        self.actionStacks_with_Subparts.setObjectName("actionStacks_with_Subparts")
        self.actionFlange_View = QtWidgets.QAction(MainWindow)
        self.actionFlange_View.setObjectName("actionFlange_View")
        self.actionWeb_View = QtWidgets.QAction(MainWindow)
        self.actionWeb_View.setObjectName("actionWeb_View")
        self.actionStiff_View = QtWidgets.QAction(MainWindow)
        self.actionStiff_View.setObjectName("actionStiff_View")
        self.actionClip_View = QtWidgets.QAction(MainWindow)
        self.actionClip_View.setObjectName("actionClip_View")
        self.actionPlate_line_View = QtWidgets.QAction(MainWindow)
        self.actionPlate_line_View.setObjectName("actionPlate_line_View")
        self.actionBurn_Drill_View = QtWidgets.QAction(MainWindow)
        self.actionBurn_Drill_View.setObjectName("actionBurn_Drill_View")
        self.actionFlange_Report = QtWidgets.QAction(MainWindow)
        self.actionFlange_Report.setObjectName("actionFlange_Report")
        self.actionWeb_Report = QtWidgets.QAction(MainWindow)
        self.actionWeb_Report.setObjectName("actionWeb_Report")
        self.actionStiff_Report = QtWidgets.QAction(MainWindow)
        self.actionStiff_Report.setObjectName("actionStiff_Report")
        self.actionClip_Report = QtWidgets.QAction(MainWindow)
        self.actionClip_Report.setObjectName("actionClip_Report")
        self.actionPlate_Report = QtWidgets.QAction(MainWindow)
        self.actionPlate_Report.setObjectName("actionPlate_Report")
        self.actionBurn_Drill_Report = QtWidgets.QAction(MainWindow)
        self.actionBurn_Drill_Report.setObjectName("actionBurn_Drill_Report")
        self.actionNC_Deal = QtWidgets.QAction(MainWindow)
        self.actionNC_Deal.setObjectName("actionNC_Deal")
        self.menuFile_F.addAction(self.actionSelect_Orders_Alt_S)
        self.menuFile_F.addAction(self.actionBatching_Alt_B)
        self.menuFile_F.addAction(self.actionNC_Deal)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.actionExit_Alt_X)
        self.menuReport_Alt_R.addAction(self.actionStack_Total_Alt_T)
        self.menuReport_Alt_R.addAction(self.actionFlange_Report)
        self.menuReport_Alt_R.addAction(self.actionWeb_Report)
        self.menuReport_Alt_R.addAction(self.actionStiff_Report)
        self.menuReport_Alt_R.addAction(self.actionClip_Report)
        self.menuReport_Alt_R.addAction(self.actionPlate_Report)
        self.menuReport_Alt_R.addAction(self.actionBurn_Drill_Report)
        self.menuView_V.addAction(self.actionShow_Batch_Report)
        self.menuView_V.addAction(self.actionStacks_with_Subparts)
        self.menuView_V.addAction(self.actionFlange_View)
        self.menuView_V.addAction(self.actionWeb_View)
        self.menuView_V.addAction(self.actionStiff_View)
        self.menuView_V.addAction(self.actionClip_View)
        self.menuView_V.addAction(self.actionPlate_line_View)
        self.menuView_V.addAction(self.actionBurn_Drill_View)
        self.menubar.addAction(self.menuFile_F.menuAction())
        self.menubar.addAction(self.menuView_V.menuAction())
        self.menubar.addAction(self.menuReport_Alt_R.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Batch"))
        self.pushButton_show_orders.setText(_translate("MainWindow", "Select Orders"))
        self.pushButton_batching.setText(_translate("MainWindow", "Batching"))
        self.pushButton_show_batch_report.setText(_translate("MainWindow", "Show Batch Report"))
        self.label.setText(_translate("MainWindow", "Step 1:"))
        self.label_2.setText(_translate("MainWindow", "Step 2:"))
        self.label_3.setText(_translate("MainWindow", "Step 3:"))
        self.label_4.setText(_translate("MainWindow", "NC File Path:"))
        self.pushButton_browse_nc_path.setText(_translate("MainWindow", "Browse"))
        self.pushButton_nc_deal.setText(_translate("MainWindow", "Deal"))
        self.pushButton_stack_with_subparts.setText(_translate("MainWindow", "Stacks with Subparts"))
        self.pushButton_stiff_view.setText(_translate("MainWindow", "Stiff View"))
        self.pushButton_burn_view.setText(_translate("MainWindow", "Burn/Drill View"))
        self.pushButton_clip_view.setText(_translate("MainWindow", "Clip View"))
        self.pushButton_plate_view.setText(_translate("MainWindow", "Plate line View"))
        self.pushButton_web_view.setText(_translate("MainWindow", "Web View"))
        self.pushButton_flange_view.setText(_translate("MainWindow", "Flange View"))
        self.pushButton_flange_report.setText(_translate("MainWindow", "Report File For Flange"))
        self.pushButton_web_report.setText(_translate("MainWindow", "Report File For Web"))
        self.pushButton_stiff_report.setText(_translate("MainWindow", "Report File For Stiff"))
        self.pushButton_clip_report.setText(_translate("MainWindow", "Report File For Clip"))
        self.pushButton_plate_report.setText(_translate("MainWindow", "Report File For Plate"))
        self.pushButton_burn_report.setText(_translate("MainWindow", "Report File For Burn"))
        self.pushButton_all_report.setText(_translate("MainWindow", "Report File For All"))
        self.label_5.setText(_translate("MainWindow", "Batch the Batch:"))
        self.label_6.setText(_translate("MainWindow", "Example: 1-5;6-10;10-15"))
        self.menuFile_F.setTitle(_translate("MainWindow", "File(&F)"))
        self.menuReport_Alt_R.setTitle(_translate("MainWindow", "Report(&R)"))
        self.menuView_V.setTitle(_translate("MainWindow", "View(V)"))
        self.actionSelect_Orders_Alt_S.setText(_translate("MainWindow", "Select Orders(&S)"))
        self.actionBatching_Alt_B.setText(_translate("MainWindow", "Batching(&B)"))
        self.actionStack_Total_Alt_T.setText(_translate("MainWindow", "Stack Total(&T)"))
        self.actionExit_Alt_X.setText(_translate("MainWindow", "Exit(&X)"))
        self.actionShow_Batch_Report.setText(_translate("MainWindow", "Show Batch Report"))
        self.actionStacks_with_Subparts.setText(_translate("MainWindow", "Stacks with Subparts"))
        self.actionFlange_View.setText(_translate("MainWindow", "Flange View"))
        self.actionWeb_View.setText(_translate("MainWindow", "Web View"))
        self.actionStiff_View.setText(_translate("MainWindow", "Stiff View"))
        self.actionClip_View.setText(_translate("MainWindow", "Clip View"))
        self.actionPlate_line_View.setText(_translate("MainWindow", "Plate line View"))
        self.actionBurn_Drill_View.setText(_translate("MainWindow", "Burn/Drill View"))
        self.actionFlange_Report.setText(_translate("MainWindow", "Flange Report"))
        self.actionWeb_Report.setText(_translate("MainWindow", "Web Report"))
        self.actionStiff_Report.setText(_translate("MainWindow", "Stiff Report"))
        self.actionClip_Report.setText(_translate("MainWindow", "Clip Report"))
        self.actionPlate_Report.setText(_translate("MainWindow", "Plate Report"))
        self.actionBurn_Drill_Report.setText(_translate("MainWindow", "Burn/Drill Report"))
        self.actionNC_Deal.setText(_translate("MainWindow", "NC Deal"))


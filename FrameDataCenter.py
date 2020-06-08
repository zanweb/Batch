# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FrameDataCenter.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 825)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.showMaximized()
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1121, 781))
        self.verticalLayoutWidget.setMinimumSize(1280, 781)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tree_widget_function_tree = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        # self.tree_widget_function_tree.setMaximumSize(QtCore.QSize(200, 16777215))\
        self.tree_widget_function_tree.setFixedWidth(200)
        self.tree_widget_function_tree.setObjectName("tree_widget_function_tree")
        self.tree_widget_function_tree.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.tree_widget_function_tree)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.frame = QtWidgets.QFrame(self.tab)
        # self.frame.setGeometry(QtCore.QRect(0, 0, 1200, 621))
        self.frame.setMinimumWidth(880)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        # self.frame_2.setGeometry(QtCore.QRect(0, 10, 1190, 591))
        self.frame_2.setMinimumWidth(870)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        # self.groupBox.setMinimumSize(QtCore.QSize(200, 780))
        self.groupBox.setFixedWidth(200)
        # self.groupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.push_button = QtWidgets.QPushButton(self.groupBox)
        self.push_button.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.push_button.setObjectName("push_button")
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.menu.addAction(self.actionImport)
        self.menubar.addAction(self.menu.menuAction())

        g_layout = QtWidgets.QGridLayout()
        self.centralwidget.setLayout(g_layout)
        # g_layout.addWidget(self.centralwidget)
        # g_layout.addWidget(self.verticalLayoutWidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.push_button.setText(_translate("MainWindow", "PushButton"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.actionImport.setText(_translate("MainWindow", "Import"))

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout, QColorDialog, QInputDialog, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QColor


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.style = """ 
                QPushButton{background-color:grey;color:white;} 
                #window{ background:pink; }
                #test{ background-color:black;color:white; }
            """
        self.setStyleSheet(self.style)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('test')
        self.setObjectName("window")

        btn1 = QPushButton("关闭", self)
        btn1.clicked.connect(self.close)
        btn1.setObjectName('test')
        btn2 = QPushButton("最小化", self)
        btn2.clicked.connect(self.showMinimized)
        btn3 = QPushButton("最大化", self)
        btn3.clicked.connect(self.showMaximized)

        btn11 = QPushButton("改变背景", self)
        btn11.clicked.connect(self.showColor)
        btn22 = QPushButton("选择文件", self)
        btn22.clicked.connect(self.showFile)
        btn33 = QPushButton("对话框", self)
        btn33.clicked.connect(self.showDialog)
        self.linet1 = QLineEdit("111111", self)
        self.linet2 = QLineEdit("ssssssss", self)

        hbox1 = QHBoxLayout()  # 水平布局
        hbox1.addWidget(btn1)
        hbox1.addWidget(btn2)
        hbox1.addWidget(btn3)
        hbox2 = QHBoxLayout()  # 水平布局
        hbox2.addWidget(btn11)
        hbox2.addWidget(btn22)
        hbox2.addWidget(btn33)
        vbox = QVBoxLayout()  # 垂直布局
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.linet1)
        vbox.addWidget(self.linet2)
        self.setLayout(vbox)

        self.show()

    # 重写三个方法使我们的Example窗口支持拖动,上面参数window就是拖动对象


    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def showColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QInputDialog.getText(self, '对话框',
                                        '请输入你的名字:')

        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
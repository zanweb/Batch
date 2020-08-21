#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/6/10 15:57
# @Author   :   ZANWEB
# @File     :   ComTools in Batch
# @IDE      :   PyCharm

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt

from collections import Iterable


class RecordIndex(QWidget):
    def __init__(self):
        super().__init__(None)
        self.index = 1
        self.records = []
        self.total = 0

        self.btn_first = QPushButton('|<')
        self.btn_first.setFixedWidth(30)
        self.btn_prev = QPushButton('<')
        self.btn_prev.setFixedWidth(30)
        self.line_index = QLineEdit()
        self.line_index.setFixedWidth(100)
        self.line_index.setAlignment(Qt.AlignRight)
        self.btn_forward = QPushButton('>')
        self.btn_forward.setFixedWidth(30)
        self.btn_last = QPushButton('>|')
        self.btn_last.setFixedWidth(30)
        self.l_total_number = QLabel(str(self.total))

        # self.ui_init()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.ui_init())
        self.setLayout(self.vbox)
        self.set_connect()

    def ui_init(self):
        group_box = QGroupBox()
        l_name = QLabel('记录:')
        l_name.setFixedWidth(30)
        l_total = QLabel('记录总数:')
        l_total.setFixedWidth(50)
        hbox = QHBoxLayout()
        hbox.addWidget(l_name)
        hbox.addWidget(self.btn_first)
        hbox.addWidget(self.btn_prev)
        hbox.addWidget(self.line_index)
        hbox.addWidget(self.btn_forward)
        hbox.addWidget(self.btn_last)
        hbox.addWidget(l_total)
        hbox.addWidget(self.l_total_number)
        group_box.setLayout(hbox)
        group_box.setFixedHeight(37)
        return group_box

    def set_resource(self, iter_item):
        if isinstance(iter_item, Iterable):
            if iter_item:
                self.records = iter_item
                self.total = len(list(iter_item))
                self.l_total_number.setText(str(self.total))
                self.line_index.setText('1')
            else:
                QMessageBox.warning(None, '警告', '数据集为空!')
        else:
            QMessageBox.warning(None, "警告", '数据集不可迭代!')

    def set_connect(self):
        self.btn_first.clicked.connect(self.on_btn_first_clicked)
        self.btn_prev.clicked.connect(self.on_btn_prev_clicked)
        self.btn_forward.clicked.connect(self.on_btn_forward_clicked)
        self.btn_last.clicked.connect(self.on_btn_last_clicked)
        self.line_index.editingFinished.connect(self.on_line_index_edit_finished)

    @pyqtSlot()
    def on_btn_first_clicked(self):
        self.line_index.setText('1')
        self.index = 1

    @pyqtSlot()
    def on_btn_prev_clicked(self):
        if self.index > 1:
            self.index -= 1
            self.line_index.setText(str(self.index))
        else:
            QMessageBox.warning(None, '警告', '已经到达记录第一条!')

    @pyqtSlot()
    def on_btn_forward_clicked(self):
        if self.index < self.total:
            self.index += 1
            self.line_index.setText(str(self.index))
        else:
            QMessageBox.warning(None, '警告', '已经到底记录最后一条!')

    @pyqtSlot()
    def on_btn_last_clicked(self):
        self.index = self.total
        self.line_index.setText(str(self.total))

    @pyqtSlot()
    def on_line_index_edit_finished(self):
        if 1 <= int(self.line_index.text()) <= self.total:
            self.index = int(self.line_index.text())
        else:
            QMessageBox.warning(None, '警告', '你的输入是错误的!')
            self.line_index.setFocus()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton
    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    r_index = RecordIndex()
    r_index.set_resource([1, 2, 3, 4, 5])
    # r_index.ui_init()
    window.setCentralWidget(r_index)
    window.show()
    sys.exit(app.exec_())

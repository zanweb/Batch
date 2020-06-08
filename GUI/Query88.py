#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QLineEdit, QLabel, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot

import pymssql
import pandas as pd


class Query(QWidget):
    def __init__(self):
        super().__init__(None)

        self.user_info = None
        self.head_list = ['ProjID', 'DateMH', 'EmpeName', 'WONo', 'PrtNo', 'Len', 'sumACT', 'sumQty',
                          'sumWt',  'OracleItem', 'sumWtPkgNo']

        self.btn_check = QPushButton(r'查询')
        self.btn_export = QPushButton(r'导出')
        self.btn_check.clicked.connect(self.on_btn_check_clicked)
        self.btn_export.clicked.connect(self.on_btn_export_clicked)

        self.radio_line = QRadioButton(r'流水线')
        self.radio_hand_weld = QRadioButton(r'手工焊')
        self.radio_paint = QRadioButton(r'油漆线')

        self.line_bng_date = QLineEdit()
        self.line_end_date = QLineEdit()
        self.line_emp_name = QLineEdit()

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setRowCount(1)
        self.table.setHorizontalHeaderLabels(self.head_list)

        self.records = ''

        self.init_ui()

    def init_ui(self):
        self.resize(550, 300)
        self.setWindowTitle(r'动态删除增加控件测试')

        self.creat_ui()

    def creat_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.create_group_radio())
        hbox.addWidget(self.create_search_condition())
        hbox.addWidget(self.create_group_btn())

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.creat_group_table())

        self.setLayout(vbox)

    def create_group_radio(self):
        group_box = QGroupBox(r'工位')
        group_box.setFixedHeight(100)

        self.radio_line.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio_line)
        vbox.addWidget(self.radio_hand_weld)
        vbox.addWidget(self.radio_paint)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        # group_box.set

        return group_box

    def create_search_condition(self):
        group_box = QGroupBox('日期/姓名')
        group_box.setFixedHeight(100)

        lb1 = QLabel(r'开始日期:')
        lb2 = QLabel(r'截至日期:')
        lb3 = QLabel(r'雇员姓名:')
        vbox_lb = QVBoxLayout()
        vbox_lb.addWidget(lb1)
        vbox_lb.addWidget(lb2)
        vbox_lb.addWidget(lb3)

        vbox_line = QVBoxLayout()
        vbox_line.addWidget(self.line_bng_date)
        vbox_line.addWidget(self.line_end_date)
        vbox_line.addWidget(self.line_emp_name)

        hbox_line = QHBoxLayout()
        hbox_line.addLayout(vbox_lb)
        hbox_line.addLayout(vbox_line)

        group_box.setLayout(hbox_line)

        return group_box

    def create_group_btn(self):
        group_box = QGroupBox(r'运行')
        group_box.setFixedHeight(100)

        vbox_btn = QVBoxLayout()
        vbox_btn.addWidget(self.btn_check)
        vbox_btn.addWidget(self.btn_export)

        group_box.setLayout(vbox_btn)

        return group_box

    def creat_group_table(self):
        group_box = QGroupBox(r'内容')
        vbox_context = QVBoxLayout()
        vbox_context.addWidget(self.table)
        group_box.setLayout(vbox_context)
        return group_box

    def get_user_info(self, user_info):
        self.user_info = user_info

    @pyqtSlot()
    def on_btn_check_clicked(self):
        print(self.user_info)
        if not self.user_info:
            QMessageBox.warning(None, '警告', '无法取得用户信息')
            return
        else:
            flag, info = self.check_parameter()
            if not flag:
                QMessageBox.warning(None, '警告', info)
                return
            try:
                conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                       self.user_info['database'])
                cursor = conn.cursor()
                if self.radio_hand_weld.isChecked():
                    cursor.execute(f"exec prcHWWOWtByDateNWO @BngDate=%s, @EndDate=%s, @empName=%s",
                                   (self.line_bng_date.text(), self.line_end_date.text(), self.line_emp_name.text()))
                if self.radio_line.isChecked():
                    cursor.execute(f"exec prcLineWOWtByDateNWO @BngDate=%s, @EndDate=%s, @empName=%s",
                                   (self.line_bng_date.text(), self.line_end_date.text(), self.line_emp_name.text()))
                if self.radio_paint.isChecked():
                    cursor.execute(f"exec prcPaintWOWtByDateNWO @BngDate=%s, @EndDate=%s, @empName=%s",
                                   (self.line_bng_date.text(), self.line_end_date.text(), self.line_emp_name.text()))
                self.records = cursor.fetchall()
                self.fill_table_with_data(self.records)
                # print(records)
            except Exception as error:
                print(error)
                raise error
            finally:
                return

    def fill_table_with_data(self, records):
        if records:
            self.table.setRowCount(len(records))
            for index_row in range(0, len(records)):
                rs = records[index_row]
                for index_col in range(0, len(rs)):
                    item = rs[index_col]
                    new_item = QTableWidgetItem(str(item))
                    self.table.setItem(index_row, index_col, new_item)

    def check_parameter(self):
        flag = True
        info = ''
        if not self.line_emp_name:
            info += ' 姓名 '
            flag = False
        if not self.line_bng_date:
            info += ' 开始日期 '
            flag = False
        if not self.line_end_date:
            info += ' 截止日期 '
            flag = False

        info = '请输入下面的信息:' + info
        return flag, info

    def on_btn_export_clicked(self):
        file_name_tmp = ''
        if self.records:
            try:
                tmp = pd.DataFrame(columns=self.head_list, data=self.records)
                print(tmp)
                if self.radio_line.isChecked():
                    file_name_tmp = 'line.csv'
                if self.radio_hand_weld.isChecked():
                    file_name_tmp = 'hand_weld.csv'
                if self.radio_paint.isChecked():
                    file_name_tmp = 'paint.csv'
                tmp.to_csv(file_name_tmp, encoding='gbk')
                QMessageBox.information(None, '信息', '导出成功!')
            except Exception as error:
                print(error)
                raise error
            finally:
                return

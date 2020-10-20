#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/6/9 21:40
# @Author   :   ZANWEB
# @File     :   Project in Batch
# @IDE      :   PyCharm

from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QTabWidget, \
    QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy, QTextEdit, QMessageBox, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QDateEdit, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from GUI.ComTools import RecordIndex
import pymssql
from CamGen import FramePart
import datetime, time
from Zfile.zPDF import PdfFile
from Zfile.zExcel import ExcelFile
import os
import itertools
import copy
import re


class UiProject(QWidget):
    def __init__(self):
        super().__init__(None)

        self.user_info = None
        self.projects = None
        self.current_project = None

        self.tab_widget = QTabWidget()
        self.tab_project_base = None
        self.frame_project_base = None
        self.tab_project_bom = None
        self.frame_project_bom = None
        self.tab_project_wo = None
        self.frame_project_wo = None

        self.record_index = RecordIndex()
        # self.current_project_index = int(self.record_index.line_index.text()-1)
        self.current_project_index = 0
        self.color_id = ['']
        self.project_type_list = ['']
        self.project_status_list = ['']
        self.project_manager_list = ['']
        self.paint_id_list = ['']
        self.project_id_list = ['']
        self.projct_name_list = ['']
        self.parts_list = []
        self.part_bom = []
        self.current_parts_index = 0
        self.current_part_bom_index = 0
        self.wo_sum = []
        self.wo = []

        self.auto_no = QLineEdit()
        self.project_no = QLineEdit()
        self.project_name = QLineEdit()
        self.project_type = QComboBox()
        self.project_status = QComboBox()
        self.project_manager = QComboBox()
        self.project_designer = QComboBox()
        self.project_wt = QLineEdit()
        self.project_qty = QLineEdit()
        self.project_address = QLineEdit()
        self.project_drawing = QLineEdit()
        self.tm_received_date = QLineEdit()
        self.so = QLineEdit()
        self.batch = QLineEdit()

        self.plan_bng = QLineEdit()
        self.plan_bng.inputMask = '0000-00-00;0'

        self.real_bng = QLineEdit()
        self.plan_shipping = QLineEdit()
        self.release_drawing = QLineEdit()
        self.print_raw = QLineEdit()
        self.shift_arrange = QLineEdit()
        self.wo_import = QLineEdit()
        self.print_label = QLineEdit()
        self.pre_paint = QComboBox()
        self.raw_bng = QLineEdit()
        self.line_bng = QLineEdit()
        self.paint_bng = QLineEdit()
        self.raw_complete = QLineEdit()

        self.plan_end = QLineEdit()
        self.real_end = QLineEdit()
        self.real_shipping = QLineEdit()
        self.data_import = QLineEdit()
        self.raw_release = QLineEdit()
        self.wo_release = QLineEdit()
        self.wo_print = QLineEdit()
        self.paint_color = QComboBox()
        self.surface_paint = QComboBox()
        self.raw_end = QLineEdit()
        self.line_end = QLineEdit()
        self.paint_end = QLineEdit()
        self.ba_complete = QLineEdit()
        self.comment = QTextEdit()

        self.btn_bom_import = QPushButton('BOM导入')
        self.btn_project_update = QPushButton('项目更新')
        self.btn_mo_list_gen = QPushButton('生成MO列表')
        self.btn_mo_import = QPushButton('MO导入')
        self.btn_mo_print = QPushButton('MO打印')

        self.comb_project_id = QComboBox()
        self.comb_project_name = QComboBox()

        self.table_parts_list = QTableWidget()
        self.parts_index = RecordIndex()
        self.table_part_bom = QTableWidget()
        self.part_bom_index = RecordIndex()
        self.table_wo_sum = QTableWidget()
        self.wo_sum_index = RecordIndex()
        self.wo_index = RecordIndex()
        self.table_wo = QTableWidget()
        self.frame_import = FramePart.DialogBOMImport()

        self.init_ui()
        # self.init_data()
        self.set_connect()

    def set_connect(self):
        try:
            self.record_index.line_index.textChanged.connect(self.project_changed)
            self.comb_project_id.currentTextChanged.connect(self.project_id_changed)
            self.comb_project_name.currentTextChanged.connect(self.project_name_changed)
            self.parts_index.line_index.textChanged.connect(self.part_changed)
            self.table_parts_list.cellClicked.connect(self.part_changed_in_table)
            # self.table_part_bom.cellClicked.connect(self.sub_part_changed_in_table)
            self.part_bom_index.line_index.textChanged.connect(self.sub_part_changed)
            self.wo_sum_index.line_index.textChanged.connect(self.wo_sum_changed)
            self.table_wo_sum.selectionModel().selectionChanged.connect(self.wo_sum_changed_in_table)
            self.wo_index.line_index.textChanged.connect(self.wo_changed)
            self.table_wo.selectionModel().selectionChanged.connect(self.wo_changed_in_table)
            # self.table_parts_list.selectionChanged.connect(self.part_changed_in_table)
            self.table_parts_list.selectionModel().selectionChanged.connect(self.part_changed_in_table)
            self.table_part_bom.selectionModel().selectionChanged.connect(self.sub_part_changed_in_table)
            self.btn_bom_import.clicked.connect(self.bom_import)
            self.btn_project_update.clicked.connect(self.project_update)
            self.btn_mo_list_gen.clicked.connect(self.on_btn_mo_list_gen_clicked)
            self.btn_mo_import.clicked.connect(self.on_btn_mo_import_clicked)
            self.btn_mo_print.clicked.connect(self.on_btn_mo_print_clicked)
        except Exception as error:
            print(error)

    @pyqtSlot()
    def on_btn_mo_print_clicked(self):
        fold_mo_pdf = QFileDialog.getExistingDirectory(self, '请指定生成MO PDF文件的文件夹')
        if fold_mo_pdf:
            pdf = PdfFile(fold_mo_pdf)
            reply = pdf.gen_mo_print(self.project_no.text(), self.user_info)

            if reply == 1:
                QMessageBox.information(None, '已保存', 'MO打印文件已保存!')
            else:
                QMessageBox.warning(None, '警告', 'MO打印文件未保存!')

    @pyqtSlot()
    def on_btn_mo_import_clicked(self):
        project_id = self.project_no.text()
        file_mo, _ = QFileDialog.getOpenFileName(self, '获取MO文件')
        print(file_mo)
        _, file_name = os.path.split(file_mo)
        file_name, ext = os.path.splitext(file_name)
        print(file_name)
        if file_name:
            if file_name != self.project_no.text():
                QMessageBox.warning(None, '警告', '当前项目ID不是MO文件名,请确认!')
                return
            file_excel = ExcelFile(file_mo)
            file_excel.openpyxl_read()
            sheet_data = file_excel.sheet
            mo_list = []
            for index, item in enumerate(sheet_data):
                tmp_line = []
                # row_len = len(item)
                for col_index, cell in enumerate(item):
                    if cell:
                        if col_index == 0:
                            tmp_line.append(cell.value.split(':')[1])
                        if col_index == 1:
                            tmp_line.append(cell.value.split('*')[0][:7])
                            tmp_line.append(cell.value.split('*')[1])
                        if col_index == 3:
                            pass
                            # tmp_line.append(index)
                        if col_index == 6:
                            tmp_line.append(cell.value)
                        if col_index == 7:
                            tmp_line.append(cell.value)
                        if col_index == 8:
                            tmp_line.append(cell.value)
                mo_list.append(tmp_line)
            mo_list_sorted = sorted(mo_list, key=(lambda x: int(re.findall(r'(\d+)', x[4])[0])))
            print(mo_list_sorted)
            mo_sum_list = []
            mo_list_fin = []
            key_func = lambda x: x[2]
            for key, group in itertools.groupby(mo_list_sorted, key_func):
                # print(key + ":", list(group))
                tmp_list = copy.deepcopy(list(group))
                # print(tmp_list)
                num = len(tmp_list)
                tmp_sum = [tmp_list[0][0], tmp_list[0][1], tmp_list[0][2], tmp_list[0][3], tmp_list[0][4],
                           tmp_list[0][5], num]
                mo_sum_list.append(tmp_sum)
                # print('-----------------', num)
                if num > 1:
                    for index in range(num):
                        tmp_list[index][2] = tmp_list[index][2] + '-' + '{:04d}'.format(index + 1)
                        # print(tmp_list[index])
                        mo_list_fin.append(tmp_list[index])
                else:
                    mo_list_fin.append(tmp_list[0])
                    # print(tmp_list[0])
            print(mo_list_fin)
            # ['2001189833', 'TGA3959', '37187743-0009', 1, '119J', 8990], ['2001189833', 'TGA3959', '37187743-0010', 1,
            # '120J', 8990]]
            print(mo_sum_list)
            # ['2001189833', 'TGA3958', '37187742', 1, '101J', 10], ['2001189833', 'TGA3959', '37187743', 1, '111J', 10]]
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cur = conn.cursor()
            try:
                if mo_sum_list:
                    sql = f"SELECT WONo FROM tblWOSum WHERE WONo='{mo_sum_list[0][2]}'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    conn.commit()
                    if result:
                        ans = QMessageBox.warning(None, '警告', '此MO-SUM已存在,是否删除重新导入?', QMessageBox.Yes | QMessageBox.No)
                        if ans == QMessageBox.Yes:
                            for item in mo_sum_list:
                                sql = f"DELETE FROM tblWOSum WHERE WONo='{item[2]}'"
                                cur.execute(sql)
                                conn.commit()
                        else:
                            return

                    for item in mo_sum_list:
                        sql = f"INSERT INTO tblWOSum(WONo, ProjID, PrtNo, Length, Qty, SWO) " \
                              f"VALUES('{item[2]}', '{self.project_no.text()}', '{item[1]}', {item[5]}, " \
                              f"{item[6]},'{item[0]}') "
                        cur.execute(sql)
                        conn.commit()
                if mo_list_fin:
                    sql = f"SELECT WONo FROM tblWO WHERE WONo='{mo_list_fin[0][2]}'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    conn.commit()
                    if result:
                        ans = QMessageBox.warning(None, '警告', '此本MO已存在,是否删除重新导入?', QMessageBox.Yes | QMessageBox.No)
                        if ans == QMessageBox.Yes:
                            for item in mo_list_fin:
                                sql = f"DELETE FROM tblWO WHERE WONo='{item[2]}'"
                                cur.execute(sql)
                                conn.commit()
                        else:
                            return

                    for item in mo_list_fin:
                        sql = f"INSERT INTO tblWO(WONo, ProjID, PrtNo, Len, Qty,PkgNo) " \
                              f"VALUES('{item[2]}', '{self.project_no.text()}', '{item[1]}', {item[5]}, " \
                              f"{item[3]}, '{item[4]}') "
                        cur.execute(sql)
                        conn.commit()
            except Exception as error:
                conn.rollback()
                QMessageBox.warning(None, '警告', 'MO未人库!\n' + str(error))
            conn.close()
            QMessageBox.information(None, '信息', 'MO已成功入库!')

    @pyqtSlot()
    def on_btn_mo_list_gen_clicked(self):
        project_id = self.project_no.text()
        folder_choose = QFileDialog.getExistingDirectory(None, '选取输出文件夹', os.getcwd())
        if folder_choose != '':
            pdf = PdfFile(folder_choose)
            reply = pdf.gen_mo_list(project_id, self.user_info)
            if reply:
                QMessageBox.information(self, '保存:', 'PDF文件已保存!\n确定后将打开目标文件夹!')
                os.chdir(folder_choose)
                folder_path = os.getcwd()
                os.system("start explorer %s" % folder_path)

    @pyqtSlot()
    def project_update(self):
        print('项目更新开始!')
        n = 'NULL'
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            # cursor = conn.cursor(as_dict=True)
            cursor = conn.cursor()
            sql = f"""
                    UPDATE tblProj SET ProjName=N'{self.project_name.text()}', \
                    ProjPropID={self.project_type.currentIndex() - 1 if self.project_type.currentIndex() != 0 else 0}, \
                    ProjStatID={self.project_status.currentIndex() - 1 if self.project_status.currentIndex() != 0 else 0}, \
                    ProjMgrID={self.project_manager.currentIndex() - 1 if self.project_manager.currentIndex() != 0 else 'NULL'}, \
                    ProjEngrID={self.project_designer.currentIndex() - 1 if self.project_designer.currentIndex() != 0 else 'NULL'}, \
                    TtlWt={float(self.project_wt.text()) if self.project_wt.text() else 0}, \
                    TtlQty={float(self.project_qty.text()) if self.project_qty.text() else 0}, \
                    SOrder={int(self.so.text()) if self.so.text() else 'NULL'}, \
                    Batch={int(self.batch.text()) if self.batch.text() else 'NULL'}, \
                    Addr=N'{self.project_address.text() if self.project_address.text() else ''}', \
                    WORel={("'" + self.wo_release.text() + "'") if self.wo_release.text() else 'NULL'}, \
                    PlanBng={("'" + self.plan_bng.text() + "'") if self.plan_bng.text() else 'NULL'}, \
                    PlanEnd={"'" + (self.plan_end.text()) + "'" if self.plan_end.text() else 'NULL'}, \
                    ActBng={("'" + self.real_bng.text() + "'") if self.real_bng.text() else 'NULL'}, \
                    ActEnd={("'" + self.real_end.text() + "'") if self.real_end.text() else 'NULL'}, \
                    PlanShipDat={("'" + self.plan_shipping.text() + "'") if self.plan_shipping.text() else 'NULL'}, \
                    ActShipDat={("'" + self.real_shipping.text() + "'") if self.real_shipping.text() else 'NULL'}, \
                    DrwMK='{self.project_drawing.text() if self.project_drawing.text() else ''}', \
                    CSRel={("'" + self.release_drawing.text() + "'") if self.release_drawing.text() else 'NULL'}, \
                    CSInDB={("'" + self.data_import.text() + "'") if self.data_import.text() else 'NULL'}, \
                    RawCutPrnt={("'" + self.print_raw.text() + "'") if self.print_raw.text() else 'NULL'}, \
                    RawCutRel={("'" + self.raw_release.text() + "'") if self.raw_release.text() else 'NULL'}, \
                    ArrgRel={("'" + self.shift_arrange.text() + "'") if self.shift_arrange.text() else 'NULL'}, \
                    WOInDB={("'" + self.wo_import.text() + "'") if self.wo_import.text() else 'NULL'}, \
                    WOPrnt={("'" + self.wo_print.text() + "'") if self.wo_print.text() else 'NULL'}, \
                    LabPrnt={("'" + self.print_label.text() + "'") if self.print_label.text() else 'NULL'}, \
                    RawCutBng={("'" + self.raw_bng.text() + "'") if self.raw_bng.text() else 'NULL'}, \
                    RawCutEnd={("'" + self.raw_end.text() + "'") if self.raw_end.text() else 'NULL'}, \
                    FabBng={("'" + self.line_bng.text() + "'") if self.line_bng.text() else 'NULL'}, \
                    FabEnd={("'" + self.line_end.text() + "'") if self.line_end.text() else 'NULL'}, \
                    PatBng={("'" + self.paint_bng.text() + "'") if self.paint_bng.text() else 'NULL'}, \
                    PatEnd={("'" + self.paint_end.text() + "'") if self.paint_end.text() else 'NULL'}, \
                    Remark=N'{self.comment.toPlainText() if self.comment.toPlainText() else 'NULL'}', \
                    ProjPntColor={self.paint_color.currentIndex() - 1 if self.paint_color.currentIndex() != 0 else 'NULL'}, \
                    PramPntID={self.pre_paint.currentIndex() - 1 if self.pre_paint.currentIndex() != 0 else 'NULL'}, \
                    FinePntID={self.surface_paint.currentIndex() - 1 if self.surface_paint.currentIndex() != 0 else 'NULL'}, \
                    BAANComp={("'" + self.ba_complete.text() + "'") if self.ba_complete.text() else 'NULL'}, \
                    UseRptComp={("'" + self.raw_complete.text() + "'") if self.raw_complete.text() else 'NULL'}, \
                    TMRelease={("'" + self.tm_received_date.text() + "'") if self.tm_received_date.text() else 'NULL'}  \
                    WHERE AutoNo={int(self.auto_no.text())}
                    """
            self.comment.toPlainText()
            cursor.execute(sql)
            conn.commit()
            QMessageBox.information(None, '信息:', '项目信息已更新!')
            self.init_data()
            self.record_index.index = 1
            self.update()
            self.repaint()
        except Exception as error:
            print(error)

    @pyqtSlot()
    def bom_import(self):
        print('bom import')
        self.frame_import.get_user_info(self.user_info)
        self.frame_import.show()

    @pyqtSlot()
    def wo_changed_in_table(self):
        self.wo_index.line_index.setText(str(self.table_wo.currentRow() + 1))
        self.wo_index.index = int(self.wo_index.line_index.text())

    @pyqtSlot()
    def wo_changed(self):
        self.table_wo.selectRow(int(self.wo_index.line_index.text()) - 1)
        self.wo_index.index = int(self.wo_index.line_index.text())

    @pyqtSlot()
    def wo_sum_changed_in_table(self):
        self.wo_sum_index.line_index.setText(str(self.table_wo_sum.currentRow() + 1))
        self.wo_sum_index.index = int(self.wo_sum_index.line_index.text())

    @pyqtSlot()
    def wo_sum_changed(self):
        self.table_wo_sum.selectRow(int(self.wo_sum_index.line_index.text()) - 1)
        self.wo_sum_index.index = int(self.wo_sum_index.line_index.text())

    @pyqtSlot()
    def sub_part_changed(self):
        self.current_part_bom_index = int(self.part_bom_index.line_index.text()) - 1
        self.table_part_bom.selectRow(self.current_part_bom_index)
        self.part_bom_index.line_index.setText(str(self.current_part_bom_index + 1))
        self.part_bom_index.index = int(self.part_bom_index.line_index.text())

    @pyqtSlot()
    def sub_part_changed_in_table(self):
        self.part_bom_index.line_index.setText(str(self.table_part_bom.currentRow() + 1))
        # self.table_part_bom.selectRow(int(self.part_bom_index.line_index.text()) - 1)
        self.part_bom_index.index = self.table_part_bom.currentRow() + 1

    @pyqtSlot()
    def part_changed_in_table(self):
        self.parts_index.line_index.setText(str(self.table_parts_list.currentRow() + 1))
        self.parts_index.index = self.table_parts_list.currentRow() + 1

    @pyqtSlot()
    def part_changed(self):
        self.current_parts_index = int(self.parts_index.line_index.text()) - 1
        self.table_parts_list.selectRow(self.current_parts_index)
        self.parts_index.line_index.setText(str(self.current_parts_index + 1))
        self.get_part_bom((self.parts_list[self.current_parts_index][1], self.parts_list[self.current_parts_index][2],
                           self.projects[int(self.record_index.line_index.text()) - 1]['ProjID']))
        self.show_part_bom(self.part_bom)

    @pyqtSlot()
    def project_name_changed(self):
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor(as_dict=True)
            cursor.execute('SELECT * FROM tblProj WHERE ProjName=%s  ORDER BY AutoNo DESC',
                           self.comb_project_name.currentText())
            self.projects = cursor.fetchall()
            self.show_project_info(self.projects[0])
            # self.fill_table_with_data(self.projects)
            self.record_index.records = self.projects
            self.record_index.total = len(self.record_index.records)
            self.record_index.l_total_number.setText(str(self.record_index.total))
            self.record_index.line_index.setText('1')
            conn.close()
            self.get_parts_list()
            self.show_parts_list(self.parts_list)

            self.get_wo_sum(self.projects[self.current_project_index]['ProjID'])
            self.show_wo_sum(self.wo_sum)

            self.get_wo(self.projects[self.current_project_index]['ProjID'])
            self.show_wo(self.wo)

        except Exception as error:
            print(error)

    @pyqtSlot()
    def project_id_changed(self):
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor(as_dict=True)
            cursor.execute('SELECT * FROM tblProj WHERE ProjID=%s  ORDER BY AutoNo DESC',
                           self.comb_project_id.currentText())
            self.projects = cursor.fetchall()
            self.show_project_info(self.projects[0])
            # self.fill_table_with_data(self.projects)
            self.record_index.records = self.projects
            self.record_index.total = len(self.record_index.records)
            self.record_index.l_total_number.setText(str(self.record_index.total))
            self.record_index.line_index.setText('1')

            conn.close()
            self.get_parts_list()
            self.show_parts_list(self.parts_list)

            self.get_wo_sum(self.projects[self.current_project_index]['ProjID'])
            self.show_wo_sum(self.wo_sum)

            self.get_wo(self.projects[self.current_project_index]['ProjID'])
            self.show_wo(self.wo)

        except Exception as error:
            print(error)

    @pyqtSlot()
    def project_changed(self):
        self.current_project_index = int(self.record_index.line_index.text()) - 1
        # print('project index:', self.current_project_index, self.projects[self.current_project_index])
        self.show_project_info(self.projects[self.current_project_index])
        self.get_parts_list()
        self.show_parts_list(self.parts_list)

        self.get_wo_sum(self.projects[int(self.record_index.line_index.text()) - 1]['ProjID'])
        self.show_wo_sum(self.wo_sum)

        self.get_wo(self.projects[int(self.record_index.line_index.text()) - 1]['ProjID'])
        self.show_wo(self.wo)

    def get_user_info(self, user_info):
        self.user_info = user_info

    def init_data(self):
        if not self.user_info:
            QMessageBox.warning(None, '警告', '无法取得用户信息')
            return
        else:
            try:
                conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                       self.user_info['database'])
                cursor = conn.cursor(as_dict=True)
                cursor.execute('SELECT * FROM tblProj ORDER BY AutoNo DESC')
                self.projects = cursor.fetchall()
                self.show_project_info(self.projects[0])
                # self.fill_table_with_data(self.projects)
                self.record_index.records = self.projects
                self.record_index.total = len(self.record_index.records)
                self.record_index.l_total_number.setText(str(self.record_index.total))
                self.record_index.line_index.setText('1')

                cursor = conn.cursor()
                cursor.execute('SELECT ColorCN FROM tblColorID')
                for item in cursor.fetchall():
                    self.color_id.append(item[0])
                # self.color_id.append('未定义')
                # print(self.color_id)
                self.paint_color.addItems(self.color_id)

                cursor.execute('SELECT ProjPropDesc FROM tblProjPropID')
                for item in cursor.fetchall():
                    self.project_type_list.append(item[0])
                # print(self.project_type_list)
                # self.project_type_list.append('未定义')
                self.project_type.addItems(self.project_type_list)
                cursor.execute('SELECT ProjStatDesc FROM tblProjStatID')
                for item in cursor.fetchall():
                    self.project_status_list.append(item[0])
                # self.project_status_list.append('未定义')
                self.project_status.addItems(self.project_status_list)
                cursor.execute('SELECT Code FROM tblPntID')
                for item in cursor.fetchall():
                    self.paint_id_list.append(item[0])
                # self.paint_id_list.append('未定义')
                self.pre_paint.addItems(self.paint_id_list)
                self.surface_paint.addItems(self.paint_id_list)

                cursor.execute('SELECT ProjID FROM tblProj ORDER BY ProjID')
                for item in cursor.fetchall():
                    self.project_id_list.append(item[0])
                self.comb_project_id.addItems(self.project_id_list)

                cursor.execute('SELECT ProjName FROM tblProj GROUP BY ProjName')
                for item in cursor.fetchall():
                    self.projct_name_list.append(item[0])
                self.comb_project_name.addItems(self.projct_name_list)

                # cursor.execute('SELECT * FROM qselManifest WHERE ProjID=%s', self.projects[0]['ProjID'])
                # for item in cursor.fetchall():
                #     self.parts_list.append(item)
                # print(self.parts_list)
                self.get_parts_list()
                self.table_parts_list.setColumnCount(len(self.parts_list[0]))
                self.table_parts_list.setRowCount(1)
                self.show_parts_list(self.parts_list)

                self.get_wo_sum(self.projects[0]['ProjID'])
                self.show_wo_sum(self.wo_sum)

                self.get_wo(self.projects[0]['ProjID'])
                self.show_wo(self.wo)

                conn.close()
            except Exception as error:
                print(error)
            finally:
                return

    def get_parts_list(self):
        self.parts_list = []
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM qselManifest WHERE ProjID=%s',
                           self.projects[self.current_project_index]['ProjID'])
            for item in cursor.fetchall():
                self.parts_list.append(item)
        except Exception as error:
            print(error)

    def show_parts_list(self, parts_list):
        self.table_parts_list.clear()
        self.table_parts_list.setRowCount(0)
        self.table_parts_list.setColumnCount(0)
        self.current_project_index = 0

        headers = ['项目号', '构件号', '构件长', '数量', '单件重', '总长', '总重', '描述', '满焊', '第2腹板', '第2翼板', '焊脚']
        if parts_list:
            self.table_parts_list.setColumnCount(len(parts_list[0]))
            self.table_parts_list.setRowCount(len(parts_list))
            self.table_parts_list.setHorizontalHeaderLabels(headers)
            for row in range(0, len(parts_list)):
                part = parts_list[row]
                for column in range(0, len(part)):
                    item = part[column]
                    if isinstance(item, float):
                        str_item = '{:.2f}'.format(item)
                    else:
                        str_item = str(item)
                    new_item = QTableWidgetItem(str_item)
                    if isinstance(item, float):
                        new_item.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                    self.table_parts_list.setItem(row, column, new_item)
                # self.table_parts_list.setRowHeight(row, 25)
            self.table_parts_list.resizeColumnsToContents()
            self.table_parts_list.resizeRowsToContents()
            # print(self.parts_list[0])
            self.parts_index.line_index.setText('1')
            self.parts_index.records = parts_list
            self.parts_index.l_total_number.setText(str(len(parts_list)))
            self.parts_index.total = len(parts_list)
            self.parts_index.index = 1

            self.table_parts_list.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_parts_list.setStyleSheet("selection-background-color:rgb(0,0,255);selection-color:white")
            self.table_parts_list.selectRow(0)

            self.get_part_bom((self.parts_list[0][1], self.parts_list[0][2],
                               self.projects[int(self.record_index.line_index.text()) - 1]['ProjID']))  # 'TPNo'
            self.show_part_bom(self.part_bom)

    def show_part_bom(self, part_bom):
        self.table_part_bom.clear()
        self.table_part_bom.setRowCount(0)
        self.table_part_bom.setColumnCount(0)
        headers = ['数量', '零件号', '描述', '厚', '宽', '长', '单重', '构件号', '总数', '总重', '总长', '比重', '项目号', '构件长', '构件号']
        if part_bom:
            self.table_part_bom.setColumnCount(len(part_bom[0]))
            self.table_part_bom.setRowCount(len(part_bom))
            self.table_part_bom.setHorizontalHeaderLabels(headers)
            for row in range(0, len(part_bom)):
                one_bom = part_bom[row]
                for column in range(0, len(one_bom)):
                    item = one_bom[column]
                    if isinstance(item, float):
                        str_item = '{:.2f}'.format(item)
                    else:
                        str_item = str(item)
                    new_item = QTableWidgetItem(str_item)
                    if isinstance(item, float):
                        new_item.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                    self.table_part_bom.setItem(row, column, new_item)
                # self.table_part_bom.setRowHeight(row, 25)
            self.table_part_bom.resizeRowsToContents()
            self.table_part_bom.resizeColumnsToContents()

            self.part_bom_index.line_index.setText('1')
            self.part_bom_index.records = part_bom
            self.part_bom_index.l_total_number.setText(str(len(part_bom)))
            self.part_bom_index.total = len(part_bom)
            self.part_bom_index.index = 1

        self.table_part_bom.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_part_bom.setStyleSheet("selection-background-color:rgb(0,0,255);selection-color:white")
        self.table_part_bom.selectRow(0)

    def get_part_bom(self, part_no):
        self.part_bom = []
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM qselPrtAssm WHERE TPNo=%s AND PrtLen=%d AND ProjID=%s', part_no)
            for item in cursor.fetchall():
                self.part_bom.append(item)
            conn.close()
        except Exception as error:
            print(error)

    def show_project_info(self, project):
        for obj in self.tab_project_base.findChildren(QLineEdit):
            obj.setText('')
        for obj in self.tab_project_base.findChildren(QTextEdit):
            obj.setText('')
        for obj in self.tab_project_base.findChildren(QComboBox):
            obj.clearEditText()
        self.auto_no.setText(str(project['AutoNo']))
        self.project_no.setText(str(project['ProjID']))
        self.project_name.setText(str(project['ProjName']))

        if isinstance(project['ProjPropID'], int):
            self.project_type.setCurrentIndex(project['ProjPropID'] + 1)
            self.project_type.setCurrentText(self.project_type.itemText(self.project_type.currentIndex()))
            # self.project_type.clearEditText()
            # print('projPropID:', project['ProjPropID'])
        if isinstance(project['ProjStatID'], int):
            self.project_status.setCurrentIndex(project['ProjStatID'] + 1)
        # print(project['ProjPropID'], "-------------", project['ProjStatID'])
        # self.project_manager.setContentsMargins(str(project['ProjMgrID']))
        # self.project_designer.setContentsMargins(str(project['ProjEngrID']))
        if project['TtlWt']:
            self.project_wt.setText(str(project['TtlWt']))
        if project['TtlQty']:
            self.project_qty.setText(str(project['TtlQty']))
        if project['Addr']:
            self.project_address.setText(str(project['Addr']))
        if project['DrwMK']:
            self.project_drawing.setText(str(project['DrwMK']))
        if project['TMRelease']:
            self.tm_received_date.setText(str(project['TMRelease']))
        if project['SOrder']:
            self.so.setText(str(project['SOrder']))
        if project['Batch']:
            self.batch.setText(str(project['Batch']))
        if project['PlanBng']:
            self.plan_bng.setText(str(datetime.datetime.strftime(project['PlanBng'], '%Y-%m-%d')))
        if project['ActBng']:
            self.real_bng.setText(str(datetime.datetime.strftime(project['ActBng'], '%Y-%m-%d')))
        if project['PlanShipDat']:
            self.plan_shipping.setText(str(datetime.datetime.strftime(project['PlanShipDat'], '%Y-%m-%d')))
        if project['CSRel']:
            self.release_drawing.setText(str(datetime.datetime.strftime(project['CSRel'], '%Y-%m-%d')))
        if project['RawCutPrnt']:
            self.print_raw.setText(str(datetime.datetime.strftime(project['RawCutPrnt'], '%Y-%m-%d')))
        if project['ArrgRel']:
            self.shift_arrange.setText(str(datetime.datetime.strftime(project['ArrgRel'], '%Y-%m-%d')))
        if project['WOInDB']:
            self.wo_import.setText(str(datetime.datetime.strftime(project['WOInDB'], '%Y-%m-%d')))
        if project['LabPrnt']:
            self.print_label.setText(str(datetime.datetime.strftime(project['LabPrnt'], '%Y-%m-%d')))

        if isinstance(project['PramPntID'], int):
            self.pre_paint.setCurrentIndex(project['PramPntID'] + 1)

        if project['RawCutBng']:
            self.raw_bng.setText(str(datetime.datetime.strftime(project['RawCutBng'], '%Y-%m-%d')))
        if project['FabBng']:
            self.line_bng.setText(str(datetime.datetime.strftime(project['FabBng'], '%Y-%m-%d')))
        if project['PatBng']:
            self.paint_bng.setText(str(datetime.datetime.strftime(project['PatBng'], '%Y-%m-%d')))
        if project['UseRptComp']:
            self.raw_complete.setText(str(datetime.datetime.strftime(project['UseRptComp'], '%Y-%m-%d')))
        if project['PlanEnd']:
            self.plan_end.setText(str(datetime.datetime.strftime(project['PlanEnd'], '%Y-%m-%d')))
        if project['ActEnd']:
            self.real_end.setText(str(datetime.datetime.strftime(project['ActEnd'], '%Y-%m-%d')))
        if project['ActShipDat']:
            self.real_shipping.setText(str(datetime.datetime.strftime(project['ActShipDat'], '%Y-%m-%d')))
        if project['CSInDB']:
            self.data_import.setText(str(datetime.datetime.strftime(project['CSInDB'], '%Y-%m-%d')))
        if project['RawCutRel']:
            self.raw_release.setText(str(datetime.datetime.strftime(project['RawCutRel'], '%Y-%m-%d')))
        if project['WORel']:
            self.wo_release.setText(str(datetime.datetime.strftime(project['WORel'], '%Y-%m-%d')))
        if project['WOPrnt']:
            self.wo_print.setText(str(datetime.datetime.strftime(project['WOPrnt'], '%Y-%m-%d')))

        if isinstance(project['ProjPntColor'], int):
            self.paint_color.setCurrentIndex(project['ProjPntColor'] + 1)
        if isinstance(project['FinePntID'], int):
            self.surface_paint.setCurrentIndex(project['FinePntID'] + 1)

        if project['RawCutEnd']:
            self.raw_end.setText(str(datetime.datetime.strftime(project['RawCutEnd'], '%Y-%m-%d')))
        if project['FabEnd']:
            self.line_end.setText(str(datetime.datetime.strftime(project['FabEnd'], '%Y-%m-%d')))
        if project['PatEnd']:
            self.paint_end.setText(str(datetime.datetime.strftime(project['PatEnd'], '%Y-%m-%d')))
        if project['BAANComp']:
            self.ba_complete.setText(str(datetime.datetime.strftime(project['BAANComp'], '%Y-%m-%d')))
        if project['Remark']:
            self.comment.setText(str(project['Remark']))

    def init_ui(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.create_query_group())
        self.create_tab_project_base()
        self.create_tab_project_bom()
        self.create_tab_project_wo()

        hbox = QHBoxLayout()
        hbox.addWidget(self.tab_widget)
        hbox.addWidget(self.create_btn_group())

        vbox.addLayout(hbox)
        vbox.addWidget(self.record_index)

        self.setLayout(vbox)

    def create_tab_project_base(self):
        self.tab_project_base = QWidget()
        self.tab_project_base.setObjectName("tab")
        self.frame_project_base = QFrame(self.tab_project_base)
        # self.frame.setGeometry(QtCore.QRect(0, 0, 1200, 621))
        self.frame_project_base.setMinimumWidth(880)
        self.frame_project_base.setFrameShape(QFrame.StyledPanel)
        self.frame_project_base.setFrameShadow(QFrame.Raised)
        self.frame_project_base.setObjectName("frame")

        vbox = QVBoxLayout()
        vbox.addWidget(self.create_project_info_grid())
        self.frame_project_base.setLayout(vbox)

        self.tab_widget.addTab(self.tab_project_base, "基本信息")

    def create_project_info_grid(self):
        group_box = QGroupBox()
        l_auto = QLabel('自动编号')
        l_project_no = QLabel('项目编号')
        l_project_name = QLabel('项目名称')
        l_project_type = QLabel('项目类型')
        l_project_status = QLabel('项目状态')
        l_project_manager = QLabel('项目经理')
        l_project_designer = QLabel('项目设计')
        l_project_wt = QLabel('合计重量')
        l_project_qty = QLabel('合计件数')
        l_project_address = QLabel('项目地址')
        l_project_drawing = QLabel('项目图号')
        l_tm_receive_data = QLabel('TM接收日')
        l_so = QLabel('SOrder')
        l_batch = QLabel('Batch')

        grid_layout = QGridLayout()
        grid_layout.addWidget(l_auto, 0, 0)
        grid_layout.addWidget(l_project_no, 1, 0)
        grid_layout.addWidget(l_project_name, 2, 0)
        grid_layout.addWidget(l_project_type, 3, 0)
        grid_layout.addWidget(l_project_status, 4, 0)
        grid_layout.addWidget(l_project_manager, 5, 0)
        grid_layout.addWidget(l_project_designer, 6, 0)
        grid_layout.addWidget(l_project_wt, 7, 0)
        grid_layout.addWidget(l_project_qty, 8, 0)
        grid_layout.addWidget(l_project_address, 9, 0)
        grid_layout.addWidget(l_project_drawing, 10, 0)
        grid_layout.addWidget(l_tm_receive_data, 11, 0)
        grid_layout.addWidget(l_so, 12, 0)
        grid_layout.addWidget(l_batch, 13, 0)
        grid_layout.addWidget(self.auto_no, 0, 1)
        grid_layout.addWidget(self.project_no, 1, 1)
        grid_layout.addWidget(self.project_name, 2, 1)
        grid_layout.addWidget(self.project_type, 3, 1)
        grid_layout.addWidget(self.project_status, 4, 1)
        grid_layout.addWidget(self.project_manager, 5, 1)
        grid_layout.addWidget(self.project_designer, 6, 1)
        grid_layout.addWidget(self.project_wt, 7, 1)
        grid_layout.addWidget(self.project_qty, 8, 1)
        grid_layout.addWidget(self.project_address, 9, 1)
        grid_layout.addWidget(self.project_drawing, 10, 1)
        grid_layout.addWidget(self.tm_received_date, 11, 1)
        grid_layout.addWidget(self.so, 12, 1)
        grid_layout.addWidget(self.batch, 13, 1)

        l_plan_bng = QLabel('计划开始')
        l_real_bng = QLabel('实际开始')
        l_plan_shipping = QLabel('计划运输')
        l_release_date = QLabel('图纸下发')
        l_print_raw = QLabel('料单打印')
        l_shift_arrange = QLabel('排班下发')
        l_wo_import = QLabel('工作令入')
        l_print_label = QLabel('标签打印')
        l_pre_paint = QLabel('底漆牌号')
        l_raw_bng = QLabel('下料开始')
        l_line_bng = QLabel('流水开始')
        l_paint_bng = QLabel('油漆开始')
        l_raw_complete = QLabel('用料结算')

        grid_layout.addWidget(l_plan_bng, 0, 2)
        grid_layout.addWidget(l_real_bng, 1, 2)
        grid_layout.addWidget(l_plan_shipping, 2, 2)
        grid_layout.addWidget(l_release_date, 3, 2)
        grid_layout.addWidget(l_print_raw, 4, 2)
        grid_layout.addWidget(l_shift_arrange, 5, 2)
        grid_layout.addWidget(l_wo_import, 6, 2)
        grid_layout.addWidget(l_print_label, 7, 2)
        grid_layout.addWidget(l_pre_paint, 8, 2)
        grid_layout.addWidget(l_raw_bng, 9, 2)
        grid_layout.addWidget(l_line_bng, 10, 2)
        grid_layout.addWidget(l_paint_bng, 11, 2)
        grid_layout.addWidget(l_raw_complete, 12, 2)
        grid_layout.addWidget(self.plan_bng, 0, 3)
        grid_layout.addWidget(self.real_bng, 1, 3)
        grid_layout.addWidget(self.plan_shipping, 2, 3)
        grid_layout.addWidget(self.release_drawing, 3, 3)
        grid_layout.addWidget(self.print_raw, 4, 3)
        grid_layout.addWidget(self.shift_arrange, 5, 3)
        grid_layout.addWidget(self.wo_import, 6, 3)
        grid_layout.addWidget(self.print_label, 7, 3)
        grid_layout.addWidget(self.pre_paint, 8, 3)
        grid_layout.addWidget(self.raw_bng, 9, 3)
        grid_layout.addWidget(self.line_bng, 10, 3)
        grid_layout.addWidget(self.paint_bng, 11, 3)
        grid_layout.addWidget(self.raw_complete, 12, 3)

        l_plan_end = QLabel('计划结束')
        l_real_end = QLabel('实际结束')
        l_real_shipping = QLabel('实际运输')
        l_data_import = QLabel('数据入库')
        l_raw_release = QLabel('料单下发')
        l_wo_release = QLabel('工作令下')
        l_wo_print = QLabel('工作令打')
        l_paint_color = QLabel('油漆颜色')
        l_surface_paint = QLabel('面漆牌号')
        l_raw_end = QLabel('下料结束')
        l_line_end = QLabel('流水结束')
        l_paint_end = QLabel('油漆结束')
        l_baan_complete = QLabel('BAAN结算')

        grid_layout.addWidget(l_plan_end, 0, 4)
        grid_layout.addWidget(l_real_end, 1, 4)
        grid_layout.addWidget(l_real_shipping, 2, 4)
        grid_layout.addWidget(l_data_import, 3, 4)
        grid_layout.addWidget(l_raw_release, 4, 4)
        grid_layout.addWidget(l_wo_release, 5, 4)
        grid_layout.addWidget(l_wo_print, 6, 4)
        grid_layout.addWidget(l_paint_color, 7, 4)
        grid_layout.addWidget(l_surface_paint, 8, 4)
        grid_layout.addWidget(l_raw_end, 9, 4)
        grid_layout.addWidget(l_line_end, 10, 4)
        grid_layout.addWidget(l_paint_end, 11, 4)
        grid_layout.addWidget(l_baan_complete, 12, 4)
        grid_layout.addWidget(self.plan_end, 0, 5)
        grid_layout.addWidget(self.real_end, 1, 5)
        grid_layout.addWidget(self.real_shipping, 2, 5)
        grid_layout.addWidget(self.data_import, 3, 5)
        grid_layout.addWidget(self.raw_release, 4, 5)
        grid_layout.addWidget(self.wo_release, 5, 5)
        grid_layout.addWidget(self.wo_print, 6, 5)
        grid_layout.addWidget(self.paint_color, 7, 5)
        grid_layout.addWidget(self.surface_paint, 8, 5)
        grid_layout.addWidget(self.raw_end, 9, 5)
        grid_layout.addWidget(self.line_end, 10, 5)
        grid_layout.addWidget(self.paint_end, 11, 5)
        grid_layout.addWidget(self.ba_complete, 12, 5)

        # grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        # grid_layout.setColumnMinimumWidth(5, 200)

        l_comment = QLabel('备注')
        grid_layout.addWidget(l_comment, 14, 0)
        grid_layout.addWidget(self.comment, 14, 1, 5, 5)

        # spacer = QSpacerItem(10, 10, QSizePolicy.Maximum)
        # spacer = QSpacerItem(10, 10)
        # grid_layout.addWidget(spacer, 0, 6)
        group_box.setFixedWidth(720)
        group_box.setLayout(grid_layout)
        return group_box

    def create_tab_project_bom(self):
        self.tab_project_bom = QWidget()
        self.tab_project_bom.setObjectName("tab_bom")
        self.frame_project_bom = QFrame(self.tab_project_bom)
        # self.frame.setGeometry(QtCore.QRect(0, 0, 1200, 621))
        self.frame_project_bom.setMinimumWidth(880)
        self.frame_project_bom.setFrameShape(QFrame.StyledPanel)
        self.frame_project_bom.setFrameShadow(QFrame.Raised)
        self.frame_project_bom.setObjectName("frame_bom")
        self.tab_widget.addTab(self.tab_project_bom, "项目清单")

        vbox = QVBoxLayout()
        vbox.addWidget(self.create_parts_list())
        vbox.addWidget(self.create_part_bom())
        self.frame_project_bom.setLayout(vbox)

    def create_parts_list(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table_parts_list)
        vbox.addWidget(self.parts_index)
        group_box.setLayout(vbox)
        group_box.setMinimumHeight(300)
        return group_box

    def create_part_bom(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table_part_bom)
        vbox.addWidget(self.part_bom_index)
        group_box.setLayout(vbox)
        group_box.setMinimumHeight(400)
        return group_box

    def create_tab_project_wo(self):
        self.tab_project_wo = QWidget()
        self.tab_project_wo.setObjectName("tab_wo")
        self.frame_project_wo = QFrame(self.tab_project_wo)
        self.frame_project_wo.setMinimumWidth(880)
        self.frame_project_wo.setFrameShape(QFrame.StyledPanel)
        self.frame_project_wo.setFrameShadow(QFrame.Raised)
        self.frame_project_wo.setObjectName("frame_wo")
        self.tab_widget.addTab(self.tab_project_wo, "工作令")

        vbox = QVBoxLayout()
        vbox.addWidget(self.create_wo_sum())
        # vbox.addWidget(self.wo_sum_index)
        vbox.addWidget(self.create_wo())
        self.frame_project_wo.setLayout(vbox)

    def get_wo_sum(self, project_id):
        self.wo_sum = []
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblWOSum WHERE ProjID=%s', project_id)
            for item in cursor.fetchall():
                self.wo_sum.append(item)
            conn.close()
            # print('wo_sum: ', self.wo_sum)
        except Exception as error:
            print(error)

    def get_wo(self, project_id):
        self.wo = []
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblWO WHERE ProjID=%s', project_id)
            for item in cursor.fetchall():
                self.wo.append(item)
            # print('wo: ', self.wo)
            conn.close()
        except Exception as error:
            print(error)

    def create_wo_sum(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table_wo_sum)
        vbox.addWidget(self.wo_sum_index)
        group_box.setLayout(vbox)
        group_box.setMinimumHeight(300)
        return group_box

    def create_wo(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table_wo)
        vbox.addWidget(self.wo_index)
        group_box.setLayout(vbox)
        group_box.setMinimumHeight(400)
        return group_box

    def show_wo_sum(self, wo_sum):
        self.table_wo_sum.clear()
        self.table_wo_sum.setRowCount(0)
        self.table_wo_sum.setColumnCount(0)
        if wo_sum:
            headers = ['工作令', '项目号', '构件号', '长度', '数量', 'sort']
            self.table_wo_sum.setRowCount(len(wo_sum))
            self.table_wo_sum.setColumnCount(len(wo_sum[0]))
            self.table_wo_sum.setHorizontalHeaderLabels(headers)
            for row in range(0, len(wo_sum)):
                one_wo = wo_sum[row]
                for column in range(0, len(one_wo)):
                    item = one_wo[column]
                    new_item = QTableWidgetItem(str(item))
                    self.table_wo_sum.setItem(row, column, new_item)

            self.table_wo_sum.resizeRowsToContents()
            self.table_wo_sum.resizeColumnsToContents()
            self.wo_sum_index.line_index.setText('1')
            self.wo_sum_index.records = wo_sum
            self.wo_sum_index.l_total_number.setText(str(len(wo_sum)))
            self.wo_sum_index.total = len(wo_sum)
            self.wo_sum_index.index = 1

            self.table_wo_sum.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_wo_sum.setStyleSheet("selection-background-color:rgb(0,0,255);selection-color:white")
            self.table_wo_sum.selectRow(0)

    def show_wo(self, wo):
        self.table_wo.clear()
        self.table_wo.setRowCount(0)
        self.table_wo.setColumnCount(0)
        if wo:
            headers = ['工作令', '项目号', '构件号', '长度', '数量', '返回', '取消', '自动编号', '包号']
            self.table_wo.setRowCount(len(wo))
            self.table_wo.setColumnCount(len(wo[0]))
            self.table_wo.setHorizontalHeaderLabels(headers)
            for row in range(0, len(wo)):
                one_wo = wo[row]
                for column in range(0, len(one_wo)):
                    item = one_wo[column]
                    new_item = QTableWidgetItem(str(item))
                    self.table_wo.setItem(row, column, new_item)

            self.table_wo.resizeRowsToContents()
            self.table_wo.resizeColumnsToContents()

            self.wo_index.line_index.setText('1')
            self.wo_index.records = wo
            self.wo_index.l_total_number.setText(str(len(wo)))
            self.wo_index.total = len(wo)
            self.wo_index.index = 1

        self.table_wo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_wo.setStyleSheet("selection-background-color:rgb(0,0,255);selection-color:white")
        self.table_wo.selectRow(0)

    def create_query_group(self):
        group_box = QGroupBox('查询')
        l_comb_project_id = QLabel('输入项目号:')
        l_comb_project_id.setFixedWidth(60)
        l_comb_project_name = QLabel('输入项目名称:')
        l_comb_project_name.setFixedWidth(60)
        hbox = QHBoxLayout()
        hbox.addWidget(l_comb_project_id)
        hbox.addWidget(self.comb_project_id)
        hbox.addWidget(l_comb_project_name)
        hbox.addWidget(self.comb_project_name)

        group_box.setLayout(hbox)

        return group_box

    def create_btn_group(self):
        group_box = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_project_update)
        vbox.addWidget(self.btn_bom_import)
        vbox.addWidget(self.btn_mo_list_gen)
        vbox.addWidget(self.btn_mo_import)
        vbox.addWidget(self.btn_mo_print)
        group_box.setLayout(vbox)
        return group_box

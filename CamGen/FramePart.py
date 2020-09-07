#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/7/2 0:09
# @Author   :   ZANWEB
# @File     :   FramePart in Batch
# @IDE      :   PyCharm

from Zfile.zExcel import ExcelFile
from Zfile import zCSV
import pprint
from operator import attrgetter
import re
import openpyxl
from PyQt5.QtWidgets import QMessageBox, QWidget, QLineEdit, QLabel, QLayout, QPushButton, QGridLayout, QGroupBox, \
    QFileDialog
import pymssql
from PyQt5.QtCore import pyqtSlot
import os


class Part:
    def __init__(self):
        super().__init__()
        self.part_no = ''
        self.description = ''
        self.weight = 0.0
        self.high = 0
        self.width = 0
        self.length = 0.0
        self.web_thickness = 0
        self.flange_thickness = 0
        self.end_plate_qty = 0
        self.stiff_qty = 0
        self.full_stiff_qty = 0
        self.is_double_weld = True
        self.is_change_section = True
        self.weld_foot = 0
        self.is_full_weld = True
        self.no_2_web = ''
        self.no_2_flange = ''
        self.man_hour = 0.0
        self.part_type_id = 0
        self.arranged_qty = 0

        self.assembly = []  # (subpart, qty)
        self.oracle_item_no = ''
        self.suffix = 0
        self.manifest_id = ''
        self.version = 0

    def init_data(self, *args):
        parameter_len = len(args)
        self.part_no = args[0] if parameter_len >= 1 else ''
        self.length = args[1] if parameter_len >= 2 else 0.0
        # self.qty = args[2] if parameter_len >= 3 else 0
        self.weight = args[3] if parameter_len >= 4 else 0.0
        self.description = args[4] if parameter_len >= 5 else ''

    def gen_raw_bom(self):
        # raw BOM 构成 [Manifestid, Version, ItemNo, Material, Weight]
        raw_bom = []
        # head_bom = ['Manifestid', 'Version', 'ItemNo', 'Material', 'Weight']
        # raw_bom.append(head_bom)
        if self.assembly:
            for sub_part in self.assembly:
                tmp_raw = [self.manifest_id, self.version, self.oracle_item_no, sub_part[1].oracle_item,
                           sub_part[1].weight * sub_part[0]]
                raw_bom.append(tmp_raw)
        return raw_bom

    def organize_data(self):
        second_web = []
        second_flange = []
        web_thickness = 0.0
        web_weight = 0.0
        flange_thickness = 0.0
        flange_weight = 0.0
        web_number = 0
        flange_number = 0
        end_plate_number = 0
        total_plate_number = 0
        sub_part_length = 0
        total_weight = 0

        # 第二腹板/翼板
        for sub_part in self.assembly:
            total_plate_number += sub_part[0]
            total_weight += sub_part[0] * float(sub_part[1].weight)
            if re.findall('WEB', sub_part[1].description):
                web_number += sub_part[0]
                if float(sub_part[1].weight) > web_weight:
                    web_thickness = float(sub_part[1].thickness)
                    web_weight = float(sub_part[1].weight)
                    self.width = float(sub_part[1].width)
                second_web.append(str(sub_part[1].thickness) + '*' + str(sub_part[1].width))
            elif re.findall('FLANGE', sub_part[1].description):
                flange_number += sub_part[0]
                if float(sub_part[1].weight) > flange_weight:
                    flange_thickness = float(sub_part[1].thickness)
                    flange_weight = float(sub_part[1].weight)
                    self.high = float(sub_part[1].width)
                second_flange.append(str(sub_part[1].thickness) + '*' + str(sub_part[1].width))
            else:
                if 14 <= float(sub_part[1].thickness) <= 45:
                    end_plate_number += sub_part[0]
                else:
                    sub_part_length += float(sub_part[1].length)
        if web_thickness:
            self.web_thickness = web_thickness
        if flange_thickness:
            self.flange_thickness = flange_thickness
        if second_web:
            second_web = list(set(second_web))
            if len(second_web) > 1:
                for second in second_web:
                    if float(second.split('*')[0]) != web_thickness:
                        self.no_2_web = second
        if second_flange:
            second_flange = list(set(second_flange))
            if len(second_flange) > 1:
                for second in second_flange:
                    if float(second.split('*')[0]) != flange_thickness:
                        self.no_2_flange = second

        # 端板数量及其他板数量
        self.full_stiff_qty = end_plate_number
        self.end_plate_qty = end_plate_number
        self.stiff_qty = total_plate_number - web_number - flange_number - end_plate_number

        # 焊脚
        if self.web_thickness < 6:
            self.weld_foot = 4
        elif self.web_thickness < 10:
            self.weld_foot = 6
        else:
            self.weld_foot = 8

        # 人工时及其他
        if self.is_double_weld:
            double_weld = 1
        else:
            double_weld = 0
        if self.is_full_weld:
            full_weld = 1
        else:
            full_weld = 0
        # sgMhr = (0.75 + 0.05 * self.weld_foot) * (1 + 0.3 * double_weld) * (
        #             10 + 0.001 * Nz(oxSubPrtLen(i))) + self.end_plate_qty * (10 + 0.002 * self.width) * (
        #                     1.82 + 0.001 * self.high) * (0.76 + 0.02 * self.flange_thickness) * (
        #                     1 + 0.2 * full_weld) + self.stiff_qty * (5 + 0.0015 * self.width) + (
        #                     6 + 0.0005 * Nz(oxSubPrtLen(i))) * (0.7 + 0.0005 * self.width) + Nz(intFullStiffQty) * 15
        self.man_hour = (0.75 + 0.05 * self.weld_foot) * (1 + 0.3 * double_weld) * (
                10 + 0.001 * sub_part_length) + self.end_plate_qty * (10 + 0.002 * self.width) * (
                                1.82 + 0.001 * self.high) * (0.76 + 0.02 * self.flange_thickness) * (
                                1 + 0.2 * full_weld) + self.stiff_qty * (5 + 0.0015 * self.width) + (
                                6 + 0.0005 * sub_part_length) * (0.7 + 0.0005 * self.width) + self.full_stiff_qty * 15
        self.weight = total_weight


class SubPart:
    def __init__(self):
        super().__init__()
        self.sub_part_no = ''
        self.description = ''
        self.thickness = 0.0
        self.width = 0.0
        self.length = 0.0
        self.weight = 0.0
        self.is_detail = True
        self.oracle_item = ''

    def init_data(self, *args):
        parameter_len = len(args)
        self.sub_part_no = args[1] if parameter_len > 1 else ''
        self.description = args[2] if parameter_len > 2 else ''
        self.thickness = args[3] if parameter_len > 3 else 0.0
        self.width = args[4] if parameter_len > 4 else 0.0
        self.length = args[5] if parameter_len > 5 else 0.0
        self.weight = args[6] if parameter_len > 6 else 0.0
        self.is_detail = True if parameter_len > 7 else False

    def organize_data(self):
        description = self.description
        self.description = ('PLATE' if description == '' else self.description)
        self.description = ('PLATE' if description == '板' else self.description)
        self.description = ('PLATE' if description == '?' else self.description)

        thickness = self.thickness
        if thickness == 4.0:
            self.thickness = 5.0
            self.weight = self.weight / 4.0 * 5.0
        elif thickness == 13.0:
            self.thickness = 14.0
            self.weight = self.weight / 13.0 * 14.0
        elif thickness == 24.0:
            self.thickness = 25.0
            self.weight = self.weight / 24.0 * 25.0
        elif thickness == 26.0:
            self.thickness = 28.0
            self.weight = self.weight / 26.0 * 28.0

    def add_project_id_to_sub_part_no(self, drawing_mark, project_id_short):
        if not re.findall(drawing_mark, self.sub_part_no):
            self.sub_part_no = self.sub_part_no + '-' + project_id_short

    def get_oracle_item(self, thickness_item_list):
        thickness = float(self.thickness)
        if float(self.thickness) > 45:
            if re.findall('ANGLE', self.description) or re.findall('SHEAR', self.description):
                thickness = 107
            else:
                thickness = 999
        for kind in thickness_item_list:
            if thickness == kind['thickness']:
                self.oracle_item = kind['item_oracle']
                break


class DialogBOMImport(QWidget):
    def __init__(self):
        super().__init__(None)
        self.line_construct_file = QLineEdit()
        self.line_ie_confirm_file = QLineEdit()
        self.line_output_folder = QLineEdit()
        self.pb_construct_file_browser = QPushButton('浏览')
        self.pb_ie_confirm_file = QPushButton('浏览')
        self.pb_output_folder = QPushButton('浏览')
        self.pb_run = QPushButton('运行')
        self.user_info = None
        self.line_project_id = QLineEdit()
        self.line_project_name = QLineEdit()

        self.ui_init()
        self.set_connect()

    def ui_init(self):
        # group_box = QGroupBox()
        label_title = QLabel('BOM Import')
        label_construct_file = QLabel('构件组成清单:')
        label_ie_confirm_file = QLabel('IE确认文件:')
        label_output_folder = QLabel('BOM输出目录:')
        label_project_id = QLabel('项目编号:')
        label_project_name = QLabel('项目名称:')
        g_layout = QGridLayout()
        g_layout.addWidget(label_title, 1, 0, 1, 2)
        g_layout.addWidget(label_project_id, 2, 0)
        g_layout.addWidget(self.line_project_id, 2, 1)
        g_layout.addWidget(label_project_name, 3, 0)
        g_layout.addWidget(self.line_project_name, 3, 1)
        g_layout.addWidget(label_construct_file, 4, 0)
        g_layout.addWidget(self.line_construct_file, 4, 1)
        g_layout.addWidget(self.pb_construct_file_browser, 4, 2)
        g_layout.addWidget(label_ie_confirm_file, 5, 0)
        g_layout.addWidget(self.line_ie_confirm_file, 5, 1)
        g_layout.addWidget(self.pb_ie_confirm_file, 5, 2)
        g_layout.addWidget(label_output_folder, 6, 0)
        g_layout.addWidget(self.line_output_folder, 6, 1)
        g_layout.addWidget(self.pb_output_folder, 6, 2)
        g_layout.addWidget(self.pb_run, 7, 0, 1, 3)
        self.setLayout(g_layout)
        self.setMinimumWidth(670)

    def set_connect(self):
        self.pb_construct_file_browser.clicked.connect(self.on_pb_construct_file_browser_clicked)
        self.pb_ie_confirm_file.clicked.connect(self.on_pb_ie_confirm_file_clicked)
        self.pb_output_folder.clicked.connect(self.on_pb_output_folder_clicked)
        self.pb_run.clicked.connect(self.on_run)

    @pyqtSlot()
    def on_pb_construct_file_browser_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(None, '请选取文件:', os.getcwd(),
                                                           'All Files (*);;Excel Files (*.xls|*.xlsx|*.xlsm)')
        if file_name != '':
            self.line_construct_file.setText(file_name)

    def on_pb_ie_confirm_file_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(None, '请选取文件:', os.getcwd(),
                                                           'All Files (*);;Excel Files (*.xlsx)')
        if file_name != '':
            self.line_ie_confirm_file.setText(file_name)

    def on_pb_output_folder_clicked(self):
        folder_choose = QFileDialog.getExistingDirectory(None, '选取文件夹', os.getcwd())
        if folder_choose != '':
            self.line_output_folder.setText(folder_choose)

    def on_run(self):
        message = ''
        if self.line_project_id.text() == '':
            message += '项目编号' + '/'
        if self.line_project_name.text() == '':
            message += '项目名称' + '/'
        if self.line_construct_file.text() == '':
            message += '构件组成清单' + '/'
        if self.line_ie_confirm_file.text() == '':
            message += 'IE确认文件' + '/'
        if self.line_output_folder.text() == '':
            message += 'BOM输出目录' + '/'

        if message:
            message = "请提供: " + message[:-1] + ' 的信息!'
            QMessageBox.warning(None, '错误', message)
            return
        import_core(self.line_construct_file.text(), self.line_ie_confirm_file.text(), self.line_output_folder.text(),
                    self.line_project_id.text(), self.line_project_name.text(), self.user_info)

    def get_user_info(self, user_info):
        self.user_info = user_info


def convert_excel_to_parts(excel_path, ie_confirmed_parts=None):
    if ie_confirmed_parts is None:
        ie_confirmed_parts = []
    ex_file = ExcelFile(excel_path)
    try:
        ex_file.xlrd_read()
        sheet_data = ex_file.remove_head_tail()
    except Exception as error:
        print(error)
        try:
            ex_file.openpyxl_read()
            sheet_data = ex_file.remove_head_tail()
        except Exception as error:
            print(error)
            try:
                ex_file.direct_read_construct()
                sheet_data = ex_file.remove_head_tail_direct_construct()
            except Exception as error:
                print(error)
                return 0
    parts_list = []
    sub_part_list = []
    tmp_part = None
    seek_flag = False
    for index in range(0, len(sheet_data)):
        tmp_line = []
        row_len = len(sheet_data[index])
        if sheet_data[index][0]:
            for cell in sheet_data[index]:
                if cell:
                    tmp_line.append(cell)
            tmp_part = Part()
            tmp_part.init_data(*tmp_line)
            parts_list.append([int(tmp_line[2]), tmp_part])
            seek_part = [tmp_part.part_no, tmp_part.length]
            seek_flag = seek_part_in_ie_confirmed_parts(seek_part, ie_confirmed_parts)
        else:
            for column_index in range(row_len):
                if sheet_data[index][column_index]:
                    tmp_line = sheet_data[index][column_index:]
                    break
            sub_part_list.sort(key=attrgetter('sub_part_no'))
            # print(tmp_part.part_no, '----', tmp_line[1], '----', tmp_line[5])
            tmp_sub_part = seek_sub_part_list(tmp_line[1], tmp_line[5], sub_part_list)
            if tmp_sub_part is None:
                tmp_sub_part = SubPart()
                tmp_sub_part.init_data(*tmp_line)
                if seek_flag:
                    sub_part_list.append(tmp_sub_part)
            tmp_part.assembly.append([int(tmp_line[0]), tmp_sub_part])
    return parts_list, sub_part_list


def seek_part_in_ie_confirmed_parts(seek_part, ie_confirmed_parts):
    """
    :param seek_part: 格式: [part_no, part_length]
    :param ie_confirmed_parts: 格式:  [[4, <__main__.Part object at 0x000002460E1A5F60>]]
    :return: find_flag
    """
    find_flag = False
    for ie_part in ie_confirmed_parts:
        if ie_part[0][:7] == seek_part[0] and int(ie_part[0][10:]) == seek_part[1]:
            find_flag = True
    return find_flag


def seek_sub_part_list(sub_part_no, sub_part_length, sub_part_list):
    sub_part_r = None
    for sub_part in sub_part_list:
        if sub_part.sub_part_no == sub_part_no:
            if sub_part.length == sub_part_length:
                sub_part_r = sub_part
                break
    return sub_part_r


def select_parts_according_ie_confirm(parts_list_all, ie_parts):
    new_parts_list = []
    # ie_parts  [['BT8621500006490', 'MEZZ BEAM', 2, 329.14, suffix, manifest, version]]
    # parts_list_all  [[2, <__main__.Part object at 0x000001EA90CA87F0>]]
    for ie_part in ie_parts:
        ie_part_no = ie_part[0][:7]
        ie_part_len = int(ie_part[0][10:])
        for part_item in parts_list_all:
            part_no = part_item[1].part_no
            part_length = int(part_item[1].length)
            if (ie_part_no == part_no) and (ie_part_len == part_length):
                part_item[1].oracle_item_no = ie_part[0]
                part_item[1].description = ie_part[1]
                part_item[1].suffix = ie_part[4]
                part_item[1].manifest_id = ie_part[5]
                part_item[1].version = ie_part[6]

                new_parts_list.append(part_item)
    return new_parts_list


def prepare_parts(ex_file_ie_path, ex_file_assembly):
    """
    根据ie导出的execl文件中标注,从构件组成清单中挑出需要的构件及零件清单
    :param ex_file_ie_path: 用底色标注过的ie导出文件
    :param ex_file_assembly: 构件组成清单
    :return: 选择的构件及零件
    """
    try:
        selected_parts = []
        selected_sub_parts = []
        ex_file_ie = ExcelFile(ex_file_ie_path)
        ex_file_ie.openpyxl_read()
        items = ex_file_ie.ie_confirm_change()
        ex_file_ie.save_xlsx()
        part_list_all, selected_sub_parts = convert_excel_to_parts(ex_file_assembly, items)
        selected_sub_parts.sort(key=attrgetter('sub_part_no'))
        selected_parts = select_parts_according_ie_confirm(part_list_all, items)
        return selected_parts, selected_sub_parts
    except Exception as err:
        QMessageBox.warning(None, '警告', str(err))  # '请关闭Excel文件后再操作!'


def save_oracle_raw_bom(oracel_raw_bom, excel_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in range(0, len(oracel_raw_bom)):
        for col in range(0, len(oracel_raw_bom[0])):
            ws.cell(row + 1, col + 1, oracel_raw_bom[row][col])
    # wb.save('oracle_bom.xlsx')
    wb.save(excel_path)


def insert_many_sub_parts(sub_parts, db_info):
    conn = pymssql.connect(db_info['server'], db_info['account'], db_info['password'], db_info['database'])
    cur = conn.cursor()
    try:
        if sub_parts:
            for sub_part in sub_parts:
                sql = f"SELECT SubPrtNo FROM tblSubPrt WHERE SubPrtNo='{sub_part.sub_part_no}' AND Len={sub_part.length}"
                cur.execute(sql)
                result = cur.fetchall()
                conn.commit()
                if result:
                    sql = f"UPDATE tblSubPrt SET Descp='{sub_part.description}', Thk={sub_part.thickness}," \
                          f"Wid={sub_part.width}, Wt={sub_part.weight}, IsDetail={1 if sub_part.is_detail else 0} " \
                          f"WHERE SubPrtNo='{sub_part.sub_part_no}' AND Len={sub_part.length}"
                    cur.execute(sql)
                    conn.commit()
                else:
                    sql = f"INSERT INTO tblSubPrt(SubPrtNo, Descp, Thk, Wid, Len, Wt, IsDetail) " \
                          f"VALUES('{sub_part.sub_part_no}', '{sub_part.description}', {sub_part.thickness}, " \
                          f"{sub_part.width}, {sub_part.length}, {sub_part.weight}, {1 if sub_part.is_detail else 0})"
                    cur.execute(sql)
                    conn.commit()
    # # 建构sub_parts输入串
    # values = sub_parts
    # # 输入数据库
    # sql = 'INSERT INTO tblSubPrt(subprtno, descp, thk, wid, len, wt, isdetail) ' \
    #       'VALUES (%s,%s,%s,%s,%s,%s,%s)'
    # try:
    #     cur.executmany(sql, values)
    #     conn.commit()
    except Exception as err:
        conn.rollback()
        QMessageBox.warning(None, '警告', '零件未人库!\n' + str(err))
    conn.close()


def insert_many_assembly(assembly_part, db_info):
    conn = pymssql.connect(db_info['server'], db_info['account'], db_info['password'], db_info['database'])
    cur = conn.cursor()
    try:
        for part in assembly_part:
            for item in part[1].assembly:
                sql = f"SELECT SubPrtNo FROM tblPrtAssm WHERE PrtNo='{part[1].part_no}'" \
                      f" AND PrtLen={part[1].length} AND SubPrtNo='{item[1].sub_part_no}'" \
                      f" AND SubPrtLen={item[1].length}"
                cur.execute(sql)
                result = cur.fetchall()
                if result:
                    sql = f"UPDATE tblPrtAssm SET Qty={item[0]} WHERE PrtNo='{part[1].part_no}'" \
                          f" AND PrtLen={part[1].length} AND SubPrtNo='{item[1].sub_part_no}'" \
                          f" AND SubPrtLen={item[1].length}"
                    cur.execute(sql)
                    conn.commit()
                else:
                    sql = f"INSERT INTO tblPrtAssm(PrtNo, SubPrtNo, PrtLen, SubPrtLen, Qty) " \
                          f"VALUES ('{part[1].part_no}', '{item[1].sub_part_no}', {part[1].length}," \
                          f"{item[1].length}, {item[0]})"
                    cur.execute(sql)
                    conn.commit()

    # # 建构sub_parts输入串
    # values = assembly
    # # 输入数据库
    #
    # sql = 'INSERT INTO tblPrtAssm(PrtNo, SubPrtNo, PrtLen, SubPrtLen, Qty) ' \
    #       'VALUES (%s,%s,%s,%s,%s)'
    # try:
    #     cur.executmany(sql, values)
    #     conn.commit()
    except Exception as err:
        conn.rollback()
        QMessageBox.warning(None, '警告', '组成清单未人库!\n' + str(err))
    conn.close()


def insert_many_part(parts, db_info):
    # 输入数据库
    conn = pymssql.connect(db_info['server'], db_info['account'], db_info['password'], db_info['database'])
    cur = conn.cursor()
    try:
        for part in parts:
            sql = f"SELECT PrtNo FROM tblPrt WHERE PrtNo='{part[1].part_no}' AND Len={part[1].length}"
            cur.execute(sql)
            result = cur.fetchall()
            if result:
                sql = f"UPDATE tblPrt SET Descp='{part[1].description}', Wt={part[1].weight}, High={part[1].high}, " \
                      f"Wid={part[1].width}, WebThk={part[1].web_thickness}, FlangeThk={part[1].flange_thickness}, " \
                      f"EndPlateQty={part[1].end_plate_qty}, StiffQty={part[1].stiff_qty}, " \
                      f"FullStiffQty={part[1].full_stiff_qty}, IsDWeld={1 if part[1].is_double_weld else 0}," \
                      f"IsChgSec={1 if part[1].is_change_section else 0}, WeldFoot={part[1].weld_foot}, " \
                      f"IsFullWeld={1 if part[1].is_full_weld else 0}, No2Web='{part[1].no_2_web}', " \
                      f"No2Flange='{part[1].no_2_flange}', PrtTypeID={part[1].part_type_id} " \
                      f"WHERE PrtNo='{part[1].part_no}' AND Len={part[1].length}"
                cur.execute(sql)
                conn.commit()
            else:
                sql = f"INSERT INTO tblPrt(PrtNo, Descp, Wt, High, Wid, Len, WebThk, FlangeThk, EndPlateQty, " \
                      f"StiffQty, FullStiffQty, IsDWeld, IsChgSec, WeldFoot, IsFullWeld, No2Web, No2Flange, MHr, " \
                      f"PrtTypeID, ArrQty) VALUES ('{part[1].part_no}', '{part[1].description}', {part[1].weight}, " \
                      f"{part[1].weight}, {part[1].high}, {part[1].length}, {part[1].web_thickness}, " \
                      f"{part[1].flange_thickness}, {part[1].end_plate_qty}, {part[1].stiff_qty}, " \
                      f"{part[1].full_stiff_qty}, {1 if part[1].is_double_weld else 0}, {1 if part[1].is_change_section else 0}, " \
                      f"{part[1].weld_foot}, {1 if part[1].is_full_weld else 0}, '{part[1].no_2_web}', '{part[1].no_2_flange}', " \
                      f"{part[1].man_hour}, {part[1].part_type_id}, {part[1].arranged_qty})"
                cur.execute(sql)
                conn.commit()

    # # 建构parts输入串
    # values = parts
    #
    # sql = 'INSERT INTO tblPrt(PrtNo, Descp, Wt, High, Wid, Len, WebThk, FlangeThk, EndPlateQty, StiffQty, FullStiffQty,' \
    #       ' IsDWeld, IsChgSec, WeldFoot, IsFullWeld, No2Web, No2Flange, MHr, PrtTypeID, ArrQty)' \
    #       'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    # try:
    #     cur.executmany(sql, values)
    #     conn.commit()
    except Exception as err:
        conn.rollback()
        QMessageBox.warning(None, '警告', '构件未人库!\n' + str(err))
    conn.close()


def insert_many_manifest(manifest_id, parts_list, db_info):
    conn = pymssql.connect(db_info['server'], db_info['account'], db_info['password'], db_info['database'])
    cur = conn.cursor()
    try:
        sql = f"SELECT ProjID FROM tblProj WHERE ProjID='{manifest_id}'"
        cur.execute(sql)
        result = cur.fetchall()

        if not result:
            print(f'请先在数据库中创建{manifest_id}项目!')
            QMessageBox.information(None, 'warn:', 'warnning')
            QMessageBox.warning(None, '警告', f'请先在数据库中创建{manifest_id}项目!')
            conn.close()
            return
        else:
            for part in parts_list:
                sql = f"SELECT TPNo FROM tblManifestTP WHERE ProjID='{manifest_id}' AND TPNo='{part[1].part_no}' " \
                      f"AND Len={part[1].length}"
                cur.execute(sql)
                result = cur.fetchall()
                if result:
                    sql = f"UPDATE tblManifestTP SET Qty={part[0]} " \
                          f"WHERE ProjID='{manifest_id}' AND TPNo='{part[1].part_no}' AND Len={part[1].length}"
                    cur.execute(sql)
                    conn.commit()
                else:
                    sql = f"INSERT INTO tblManifestTP(ProjID, TPNo, Len, Qty) VALUES " \
                          f"('{manifest_id}', '{part[1].part_no}', {part[1].length}, {part[0]})"
                    cur.execute(sql)
                    conn.commit()

    # # 建构sub_parts输入串
    # values = parts_list
    # # 输入数据库
    #
    # sql = 'INSERT INTO tblManifestTP(ProjID, TPNo, Len, Qty) ' \
    #       'VALUES (%s,%s,%s,%s)'
    # try:
    #     cur.executmany(sql, values)
    #     conn.commit()
    except Exception as err:
        conn.rollback()
        QMessageBox.warning(None, '警告', '项目清单未人库!\n' + str(err))
    conn.close()


def insert_project(db_info, manifest_id, project_name='', project_prop_id=0, project_status_id=0, project_qyt=0,
                   project_weight=0.0):
    conn = pymssql.connect(db_info['server'], db_info['account'], db_info['password'], db_info['database'])
    # conn_str = r"DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % \
    #            (db_info['server'], db_info['database'], db_info['account'], db_info['password'])
    # conn = pyodbc.connect(conn_str, unicode_results=True)
    cur = conn.cursor()
    try:
        sql = f"SELECT ProjID FROM tblProj WHERE ProjID='{manifest_id}'"
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            sql = f"INSERT INTO tblProj(ProjID, ProjName, ProjPropID, ProjStatID, TtlQty, TtlWt) VALUES " \
                  f"(N'{manifest_id}', N'{project_name}', {project_prop_id}, {project_status_id}, " \
                  f"{project_qyt}, {project_weight})"
            # cur.execute("set names 'cp936'")
            cur.execute(sql)
            conn.commit()
        else:
            sql = f"UPDATE tblProj SET ProjName=N'{project_name}', ProjPropID={project_prop_id}, " \
                  f"ProjStatID={project_status_id}, TtlQty={project_qyt}, TtlWt={project_weight} " \
                  f"WHERE ProjID=N'{manifest_id}'"
            cur.execute(sql)
            conn.commit()
    except Exception as err:
        conn.rollback()
        QMessageBox.warning(None, '警告', '新项目未人库!\n' + str(err))
    conn.close()


def import_core(excel_path_construction, ex_file_ie, raw_bom_path, manifest_id, project_name, user_info):
    total_parts_num = 0
    total_parts_weight = 0.0
    # thick_item_file = zCSV.CsvFile('../FrameItems.csv')
    thick_item_file = zCSV.CsvFile('FrameItems.csv')
    thick_item_list = thick_item_file.get_frame_items()

    ex_file_raw_bom = os.path.join(raw_bom_path, str(manifest_id) + '_' + 'oracle_bom.xlsx')
    # excel_path_construction = 'C:\\Users\\zzimo\\Desktop\\构件清单\\20-2000793001-构件组成清单.xls'
    # ex_file_ie = ExcelFile('C:\\Users\\zzimo\\Desktop\\构件清单\\1\\2000793001-2211-001C IE.xlsx')

    select_parts, select_sub_parts = prepare_parts(ex_file_ie, excel_path_construction)
    select_sub_parts.sort(key=attrgetter('sub_part_no'))
    draw_mark = select_parts[0][1].part_no[:2]
    # project_id = select_parts[0][1].manifest_id.split('-')[0]
    project_id = manifest_id

    for sub_part_tmp in select_sub_parts:
        sub_part_tmp.organize_data()
        sub_part_tmp.get_oracle_item(thick_item_list)
        sub_part_tmp.add_project_id_to_sub_part_no(draw_mark, project_id.split('-')[0])
    # gen raw_bom
    material_bom = []
    head_bom = ['Manifestid', 'Version', 'ItemNo', 'Material', 'Weight']
    material_bom.append(head_bom)
    for select_part in select_parts:
        material_bom.extend(select_part[1].gen_raw_bom())
    save_oracle_raw_bom(material_bom, ex_file_raw_bom)

    for part in select_parts:
        part[1].organize_data()
        total_parts_num += part[0]
        total_parts_weight += part[0] * part[1].weight

    insert_many_sub_parts(select_sub_parts, user_info)
    insert_many_part(select_parts, user_info)
    insert_many_assembly(select_parts, user_info)
    string = project_name
    insert_project(user_info, manifest_id, string, 0, 0, total_parts_num, total_parts_weight)
    insert_many_manifest(manifest_id, select_parts, user_info)
    QMessageBox.information(None, '信息:', '数据处理完成!')


def test02():
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton
    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    frame_dialog = DialogBOMImport()
    # frame_dialog.show()
    window.setCentralWidget(frame_dialog)
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    pass

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/9/5 13:04
# @Author   :   ZANWEB
# @File     :   zPDF.py in Batch
# @IDE      :   PyCharm

from fpdf import FPDF
import os
import pymssql


class PdfFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def gen_mo_list(self, project_id, user_info):
        pdf = PdfMOList()
        pdf.get_project_id(project_id)
        pdf.get_user_info(user_info)
        pdf.pre_data()
        pdf.context()
        pdf.pre_init()

        reply = pdf.save(self.file_path)
        return reply


class PdfMOList(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('仿宋', '', r'c:\windows\fonts\simfang.ttf', uni=True)

        self.c_headers = ['工作令', '包号', '数量', '构件号', '描述', '重量', '总重量', '高', '宽',
                          '长', '腹板厚', '翼板厚', '备注']
        self.c_headers_width = [30, 10, 10, 20, 20, 15, 20, 8, 8, 15, 10, 10, 14]
        self.line_high = 5
        self.project_id = ''
        self.user_info = {}
        self.wo = []
        self.project_name = ''
        self.project_so = ''
        self.project_batch = ''
        self.project_pm = ''
        self.pre_paint = ''
        self.paint_color = ''
        self.shipping_date = ''
        self.project_info = []
        self.wo_lines = 0
        self.project_total_qty = 0
        self.project_total_wt = 0.0

        self.alias_nb_pages()

    def get_user_info(self, user_info):
        self.user_info = user_info

    def get_project_id(self, project_id):
        self.project_id = project_id

    def pre_data(self):
        self.get_wo()

    def pre_init(self):
        # self.add_page()
        pass

    def header(self):
        self.set_font('仿宋', '', 12)
        self.set_line_width(0.5)
        self.line(10, 10, 200, 10)
        self.line(10, 11, 200, 11)
        self.cell(20, 8, '项目号:', 0, 0, 'L')
        self.cell(50, 8, self.project_id, 0, 0, 'C')
        self.cell(20, 8, '项目名称:', 0, 0, 'L')
        self.cell(80, 8, self.project_name if self.project_name else '', 0, 0, 'C')
        self.cell(30, 8, '工作令', 0, 1, 'L')
        self.set_line_width(0.3)
        self.line(10, 18, 200, 18)
        self.set_font('仿宋', '', 10)
        self.cell(20, 8, '订单号:', 0, 0, 'L')
        self.cell(30, 8, (str(self.project_so) if self.project_so else ''), 0, 0, 'C')
        self.cell(20, 8, 'Batch:', 0, 0, 'L')
        self.cell(30, 8, str(self.project_batch) if self.project_batch else '', 0, 0, 'C')
        self.cell(15, 8, '总件数:', 0, 0, 'L')
        self.cell(20, 8, str(self.project_total_qty) if self.project_total_qty else '', 0, 0, 'C')
        self.cell(20, 8, '总重量:', 0, 0, 'L')
        self.cell(30, 8, format(self.project_total_wt, '0.3f') if self.project_total_wt else '', 0, 1, 'C')

        self.set_font('仿宋', '', 8)
        self.cell(20, 5, '项目经理:', 0, 0, 'L')
        self.cell(30, 5, self.project_pm if self.project_pm else '', 0, 0, 'C')
        self.cell(20, 5, '底漆:', 0, 0, 'L')
        self.cell(30, 5, self.pre_paint if self.pre_paint else '', 0, 0, 'C')
        self.cell(10, 5, self.paint_color if self.paint_color else '', 1, 0, 'C')
        self.cell(20, 5, '运输日期:', 0, 0, 'L')
        self.cell(30, 5, str(self.shipping_date) if self.shipping_date else '', 0, 1, 'C')
        self.line(10, 32, 200, 32)
        self.line(10, 33, 200, 33)

        self.set_y(33.5)
        self.set_line_width(0.1)
        line_h = self.line_high
        line_w = self.c_headers_width
        line_headers = self.c_headers
        for index, line in enumerate(self.c_headers):
            line_width = line_w[index]
            if index == (len(line_headers) - 1):
                self.cell(line_width, line_h, line, 1, 1, 'L')
            else:
                self.cell(line_width, line_h, line, 1, 0, 'L')

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-10)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def context(self):
        self.add_page()
        line_w = self.c_headers_width
        line_h = self.line_high
        if self.wo:
            for item in self.wo:
                for index, col in enumerate(line_w):
                    col_w = line_w[index]
                    if index == (len(line_w) - 1):
                        self.cell(col_w, line_h, '', 1, 1, 'L')
                    else:
                        p_string = ''
                        if isinstance(item[index], float):
                            # p_string = '0.3f'.str(item[index])
                            p_string = format(item[index], '0.2f')
                        else:
                            p_string = str(item[index])
                        self.cell(col_w, line_h, p_string, 1, 0, 'L')

    def save(self, file_path):
        try:
            path = os.path.join(file_path, self.project_id + 'MO_list.pdf')
            self.output(path, 'F')
            return 1
        except Exception as error:
            print(error)
            return 0

    def get_wo(self):
        self.wo = []
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()
            sql = f"SELECT tblWO.WONo, tblWO.PkgNo, tblWO.Qty, tblWO.PrtNo, tblPrt.Descp, tblPrt.Wt, tblPrt.Wt*tblWO.Qty AS ttl_wt, tblPrt.High, tblPrt.Wid, tblPrt.Len, tblPrt.WebThk, tblPrt.FlangeThk  FROM tblWO INNER JOIN tblPrt ON tblWO.PrtNo=tblPrt.PrtNo AND tblWO.Len=tblPrt.Len INNER JOIN tblManifestTP ON dbo.tblWO.ProjID = dbo.tblManifestTP.ProjID AND dbo.tblWO.PrtNo = dbo.tblManifestTP.TPNo AND dbo.tblWO.Len = dbo.tblManifestTP.Len WHERE tblWO.ProjID='{self.project_id}'"
            cursor.execute(sql)
            for item in cursor.fetchall():
                self.wo.append(item)
            # print('wo: ', self.wo)

            sql = f"""
                SELECT tblProj.ProjName, tblProj.SOrder, tblProj.Batch, tblProj.ProjMgrID, tblProj.PramPntID,
                tblProj.ProjPntColor, tblProj.PlanShipDat, TtlQty, TtlWt
                FROM tblProj WHERE ProjID='{self.project_id}'
                """
            cursor.execute(sql)
            for item in cursor.fetchall():
                self.project_info.append(item)

            self.project_name = self.project_info[0][0]     # 'ProjName']
            self.project_so = self.project_info[0][1]       # 'SOrder']
            self.project_batch = self.project_info[0][2]    # 'Batch']
            project_pm_id = self.project_info[0][3]         # 'ProjMgrID']
            project_paint_id = self.project_info[0][4]      # 'PramPntID']
            project_paint_color = self.project_info[0][5]   # 'ProjPntColor']
            self.shipping_date = self.project_info[0][6]    # 'PlanShipDat']
            self.project_total_qty = self.project_info[0][7]
            self.project_total_wt = self.project_info[0][8]

            if project_paint_id:
                sql = f"SELECT Code FROM tblPntID WHERE PntID='{project_paint_id}'"
                cursor.execute(sql)
                p_code = []
                for item in cursor.fetchall():
                    p_code.append(item)
                self.pre_paint = p_code[0]['Code']
            if project_paint_color:
                sql = f"SELECT ColorCN FROM tblColorID WHERE ColorID={project_paint_color}"
                cursor.execute(sql)
                p_color = []
                for item in cursor.fetchall():
                    p_color.append(item)
                self.paint_color = p_color[0][0]    # 'ColorCN']
            if project_pm_id:
                sql = f"SELECT NameEN FROM tblPhone WHERE AutoNo={project_pm_id}"
                cursor.execute(sql)
                p_pm = []
                for item in cursor.fetchall():
                    p_pm.append(item)
                self.project_pm = p_pm[0]['NameEN']

            conn.close()
        except Exception as error:
            print(error)

    def get_project_info(self, project_id):
        try:
            conn = pymssql.connect(self.user_info['server'], self.user_info['account'], self.user_info['password'],
                                   self.user_info['database'])
            cursor = conn.cursor()

            sql = f"""
                SELECT tblProj.ProjName, tblProj.SOrder, tblProj.Batch, tblProj.ProjMgrID,
                tblProj.PramPntID, tblProj.ProjPntColor, tblProj.PlanShipDat  FROM tblProj 
                WHERE ProjID={self.project_id}
                """
            cursor.execute(sql)
            project_info = cursor.fetchall()

        except Exception as error:
            print(error)


def test01():
    path = './'
    pdf_mo_list = PdfFile(path)
    user_data = {'server': '127.0.0.1\stlsojsvr04', 'database': 'MFGMISCSSQL', 'account': 'zyq', 'password': 'zyq123'}
    pdf_mo_list.gen_mo_list('1901204501-2221-014C', user_data)


if __name__ == '__main__':
    test01()

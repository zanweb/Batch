from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QCursor

from os import *
import pandas as pd
from datetime import date
import configparser
import re

from main_window import *
from CamgenInterface import *
# from Camgen import *
from CamGen import *

# all_order = c_get_all_orders()
# print(all_order[0]['ProjName'])

from stack_all import *
from stack_subpart import *
from batch_login_code import LoginDialog
from all_orders import AllOrders
from stack_stiff import StackStiff
from stack_burn import StackBurn
from stack_clip import StackClip
from stack_Plat import StackPlate
from stack_web import StackWeb
from stack_flange import StackFlange


class MyPushbutton(QtWidgets.QPushButton):
    inp_text_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super(MyPushbutton, self).__init__(parent)

    def focusInEvent(self, QFocusEvent):
        self.setStyleSheet("background-color:green;")
        print('Focus in')

    def focusOutEvent(self, QFocusEvent):
        print('Focus out')

    def mouseMoveEvent(self, *args, **kwargs):
        print('Mouse move')

    def LEAVEEVENT(self, e):  # 鼠标离开label
        self.setStyleSheet("background-color:lightgray;")
        # self.resize(self.sizeHint())
        self.resize(QSize(141, 51))
        print('leaveEvent')

    def enterEvent(self, e):  # 鼠标移入label
        try:
            self.setStyleSheet("background-color:blue;")
            self.resize(QSize(141, 51))
            print('enterEvent')
        except Exception as ev:
            print(ev)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # class MainWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # super(MainWindow, self).__init__()
        # self.MyCombo = QComboBox()Ui_MainWindow
        self.setupUi(self)
        self.loginD = LoginDialog()
        # self.status_bar = QStatusBar(parent=self)
        self.initui()

        # self.pushButton_show_orders.mouseMoveEvent.connect(self.mouse_move)
        # self.pushButton_show_orders = MyPushbutton(self.centralwidget)
        # self.pushButton_show_orders.setGeometry(QRect(30, 70, 141, 51))
        # self.pushButton_show_orders.setObjectName('pushButton_show_orders')
        # self.pushButton_show_orders.setText('Select Order')
        self.pushButton_show_orders.clicked.connect(self.show_orders)
        self.loginD.pushButton.clicked.connect(self.get_user_info)
        self.pushButton_batching.clicked.connect(self.get_batch)
        self.pushButton_show_batch_report.clicked.connect(self.report_stack_total)
        self.pushButton_browse_nc_path.clicked.connect(self.browse_nc_path)
        self.pushButton_nc_deal.clicked.connect(self.nc_deal)
        self.pushButton_stack_with_subparts.clicked.connect(self.report_stack_with_subparts)
        self.pushButton_stiff_view.clicked.connect(self.stiff_view)
        self.pushButton_burn_view.clicked.connect(self.burn_view)
        self.pushButton_clip_view.clicked.connect(self.clip_view)
        self.pushButton_plate_view.clicked.connect(self.plate_view)
        self.pushButton_web_view.clicked.connect(self.web_view)
        self.pushButton_flange_view.clicked.connect(self.flange_view)

        self.pushButton_all_report.clicked.connect(self.all_report)
        self.pushButton_flange_report.clicked.connect(self.flange_report)
        self.pushButton_web_report.clicked.connect(self.web_report)
        self.pushButton_stiff_report.clicked.connect(self.stiff_report)
        self.pushButton_clip_report.clicked.connect(self.clip_report)
        self.pushButton_plate_report.clicked.connect(self.plate_report)
        self.pushButton_burn_report.clicked.connect(self.burn_report)

        self.actionExit_Alt_X.triggered.connect(self.close)
        self.actionBatching_Alt_B.triggered.connect(self.get_batch)

        self.actionBurn_Drill_Report.triggered.connect(self.burn_report)
        self.actionClip_Report.triggered.connect(self.clip_report)
        self.actionPlate_Report.triggered.connect(self.plate_report)
        self.actionWeb_Report.triggered.connect(self.web_report)
        self.actionFlange_Report.triggered.connect(self.flange_report)
        self.actionStiff_Report.triggered.connect(self.stiff_report)
        self.actionStack_Total_Alt_T.triggered.connect(self.all_report)

        self.actionBurn_Drill_View.triggered.connect(self.burn_view)
        self.actionStiff_View.triggered.connect(self.stiff_view)
        self.actionClip_View.triggered.connect(self.clip_view)
        self.actionPlate_line_View.triggered.connect(self.plate_view)
        self.actionWeb_View.triggered.connect(self.web_view)
        self.actionFlange_View.triggered.connect(self.flange_view)

        self.user_info = []
        self.user_account = ''
        self.user_password = ''
        self.server = ''
        self.database = ''
        self.tableWidget_orders = AllOrders()  # 获取订单
        self.all_order = []
        # self.tableWidget_orders.select_exit.connect(self.get_orders)
        # self.tableWidget_orders.contextMenuEvent(QContextMenuEvent=)
        self.orders = []
        self.batch_c = BATCH()
        self.report_stack_form = StackAll()
        self.report_with_subparts = StackSubpart()
        self.nc_file_path = ''
        self.report_stack_stiff = StackStiff()
        self.report_stack_burn = StackBurn()
        self.report_stack_clip = StackClip()
        self.report_stack_plate = StackPlate()
        self.report_stack_web = StackWeb()
        self.report_stack_flange = StackFlange()
        self.batch_state = 0
        self.by_web_or_flange = 0  # 默认by web , 设置文件中设置为1则by flange
        self.limit_flange_wt = 4500
        self.limit_web_wt = 4500
        self.pd_heads = ['StackNo', 'SeqNo', 'SubPartNo', 'Qty', 'QtyPSeq', 'Thk', 'Wid', 'SubPartLen',
                         'SubPartLenPSeq', 'Wt', 'WtPSeq', 'HasHole', 'HoleList', 'SubType',
                         'PartNo', 'PartLen', 'PartQty', 'PartDesc', 'OrderNo']
        self.writer = ''
        self.out_fold = ''

    # def __del__(self):
    #     del self.batch_c, self.loginD, self.tableWidget_orders

    def initui(self):
        # self.statusBar.setBaseSize(100, 30)
        self.statusBar.showMessage('Message: Select the Orders, Please!')

    def get_man_hour(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        man_hour_stack = []
        for seq in self.batch_c.stacks:
            man_hour_detail = {'StackNo': seq[0],
                               'SeqNo': seq[1],
                               'Manhour_web/Seq': seq[2].man_hour_web * seq[3],
                               'Manhour_flange/Seq': seq[2].man_hour_flange * seq[3],
                               'Manhour_plate/Seq': seq[2].man_hour_plate * seq[3],
                               'Manhour_line/Seq': seq[2].man_hour_line * seq[3],
                               'Manhour_HW/Seq': seq[2].man_hour_hw * seq[3],
                               'PartNo': seq[2].no,
                               'PartLen': seq[2].len,
                               'PartQty': seq[3],
                               'PartDesc': seq[2].dec,
                               'OrderNo': seq[4]
                               }
            man_hour_stack.append(man_hour_detail)
        return man_hour_stack

    def get_all_sub_part_by_type(self, type):
        sub_parts_list = self.get_all_list()
        need_list = []
        for sub_part in sub_parts_list:
            if sub_part['SubType'] == type:
                need_list.append(sub_part)
        return need_list

    def create_out_fold(self):
        self.out_fold = QFileDialog.getExistingDirectory(None, 'Please Indicate Out fold!')
        if not os.path.exists(self.out_fold + '/FMI_Flange'):
            os.makedirs(self.out_fold + '/FMI_Flange')
        if not os.path.exists(self.out_fold + '/Ped_Flange'):
            os.makedirs(self.out_fold + '/Ped_Flange')

    def flange_nc_to_ped(self):
        batch_list = self.get_all_sub_part_by_type(2)
        print(batch_list)
        in_fold = self.nc_file_path
        out_fold = self.out_fold + '/Ped_Flange'
        ped_trans(batch_list, in_fold, out_fold)

    def flange_nc_to_fmi(self):
        batch_list = self.get_all_sub_part_by_type(2)
        print(batch_list)
        in_fold = self.nc_file_path
        out_fold = self.out_fold + '/FMI_Flange'
        fmi_flange_trans(batch_list, in_fold, out_fold)
        fmi_flange_trans_single_file(batch_list, in_fold, out_fold)

    def get_all_list(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        data_stack = []
        # data_detail = {}
        for seq in self.batch_c.stacks:
            for sub in seq[2].subparts:
                data_detail = {}
                data_detail = {'StackNo': seq[0],
                               'SeqNo': seq[1],
                               'OrderNo': seq[4],
                               'PartNo': seq[2].no,
                               'PartLen': seq[2].len,
                               'PartQty': seq[3],
                               'PartDesc': seq[2].dec,
                               'SubPartNo': sub[0].no,
                               'SubPartLen': sub[0].len,
                               'Qty': sub[1],
                               'QtyPSeq': sub[1] * seq[3],
                               'Thk': sub[0].thk,
                               'Wid': sub[0].wid,
                               'Wt': sub[0].wt,
                               'WtPSeq': sub[0].wt * sub[1] * seq[3],
                               'HasHole': sub[0].has_hole,
                               'HoleList': sub[0].holes_dia,
                               'SubType': sub[0].type,
                               'SubPartLenPSeq': sub[0].len * sub[1] * seq[3]}
                data_stack.append(data_detail)
        return data_stack

    def mouse_move(self):
        button = main_show.sender()
        button.resize(150, 75)

    def format_excel(self):
        try:
            for worksheet in self.writer.book.worksheets():
                if worksheet.name.find('Seq') != -1:
                    worksheet.set_zoom(75)
                    worksheet.set_print_scale(65)
                    worksheet.set_landscape()
                    worksheet.set_paper(9)
                    worksheet.set_margins(left=0.3, right=0.1, top=0.5, bottom=0.5)
                    worksheet.set_header('&C&"Courier New,Bold"Worklist Report')
                    worksheet.set_footer('&R&P of &N')
                    worksheet.repeat_rows(0, 6)
                    worksheet.set_column('C:C', 15)
                    worksheet.set_column('M:M', 18)
                    worksheet.set_column('S:S', 22)
                if worksheet.name.find('Plan') != -1:
                    worksheet.set_column('F:F', 12)
                    worksheet.set_column('J:L', 12)
                    worksheet.set_column('N:N', 22)
                    worksheet.set_column('O:P', 12)
                    worksheet.set_margins(left=0.7)
        except Exception as e:
            print(e)
        finally:
            return

    def xls_report_header(self, header):
        create_date = "{:%m-%d-%Y}".format(date.today())
        create_by = self.user_account
        footer = [('Create By', [create_by]), ('Version', [0.1]), ('Creat Date', [create_date]),
                  ('Weight Unit', ['kg']), ('Length Unit', ['mm'])]
        df_footer = pd.DataFrame.from_items(footer)
        df_footer.to_excel(self.writer, index=False, sheet_name=(header + ' Seq'))
        df_footer.to_excel(self.writer, index=False, sheet_name=(header + ' Raw'))
        headers = [('Department', [header]),
                   ('Order Area', [self.batch_c.area]),
                   ('Orders', [self.orders])]
        df_header = pd.DataFrame.from_items(headers)
        df_header.to_excel(self.writer, startrow=3, index=False, sheet_name=(header + ' Seq'), freeze_panes=[7, 0])
        df_header.to_excel(self.writer, startrow=3, index=False, sheet_name=(header + ' Raw'))

    def xls_report_all(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        # df = df.loc[df['SubType'] == 2]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='All Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['All Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='All Raw')

    def xls_report_flange(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 2]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Flange Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Flange Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Flange Raw')

    def xls_report_web(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 1]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Web Seq')
        number_rows_all = len(df.index)
        # print(number_rows_all)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Web Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Web Raw')

    def xls_report_stiff(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 3]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Stiff Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Stiff Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Stiff Raw')

    def xls_report_clip(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 4]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Clip Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Clip Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Clip Raw')

    def xls_report_plate(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 6]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Plate Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Plate Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Plate Raw')

    def xls_report_burn(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[df['SubType'] == 5]
        df = df.sort_values(['StackNo', 'SubPartLen', 'Wt'], ascending=[True, False, False])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Burn Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Burn Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = 0
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if int(row['StackNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = int(row['StackNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='Burn Raw')

    def xls_report_man_hour(self):
        man_hour = self.get_man_hour()
        df = pd.DataFrame(man_hour, columns=['StackNo', 'SeqNo', 'Manhour_web/Seq', 'Manhour_flange/Seq',
                                             'Manhour_plate/Seq', 'Manhour_line/Seq', 'Manhour_HW/Seq',
                                             'PartNo', 'PartLen', 'PartQty', 'PartDesc', 'OrderNo'])
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Man_hour Seq')
        number_rows_all = len(df.index)
        if number_rows_all != 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['Man_hour']
            cell_range = 'C7:J' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('C8:G' + str(number_rows_all + 7), 9, format_number)

    def get_stacks_list(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        data_stack = []
        for seq in self.batch_c.stacks:
            data_detail = {'StackNo': seq[0],
                           'SeqNo': seq[1],
                           'PartNo': seq[2].no,
                           'PartLen': seq[2].len,
                           'PartQty': seq[3],
                           'PartDesc': seq[2].dec,
                           'WebThk': seq[2].web[0].thk,
                           'WebWid': seq[2].web[0].wid,
                           'WebWt': int(seq[2].web_wt * seq[3] * 1000) / 1000,
                           'FlangeThk': seq[2].flange[0].thk,
                           'FlangeWid': seq[2].flange[0].wid,
                           'FlangeWt': int(seq[2].flange_wt * seq[3] * 1000) / 1000,
                           'SeqWt': int(seq[2].wt * seq[3] * 1000) / 1000,
                           'OrderNo': seq[4],
                           'Sec_web': seq[2].second_web,
                           'Sec_flange': seq[2].second_flange
                           }
            data_stack.append(data_detail)
        return data_stack

    def xls_report_plan(self):
        headers = ['StackNo',
                   'SeqNo',
                   'PartNo',
                   'PartLen',
                   'PartQty',
                   'PartDesc',
                   'WebThk',
                   'WebWid',
                   'WebWt',
                   'FlangeThk',
                   'FlangeWid',
                   'FlangeWt',
                   'SeqWt',
                   'OrderNo',
                   'Sec_web',
                   'Sec_flange']
        df = pd.DataFrame(self.get_stacks_list(), columns=headers)
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='Plan Seq')
        workbook = self.writer.book
        worksheet = self.writer.sheets['Plan Seq']
        format_top_border = workbook.add_format()
        format_top_border.set_top()
        old_value = 0
        row_fix = 6
        for index, row in df.iterrows():
            row_fix += 1
            if int(row['StackNo']) != old_value:
                worksheet.set_row(row_fix, None, format_top_border)
                old_value = int(row['StackNo'])

    def xls_report_no_web_flange(self):
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[(df['SubType'] != 1) & (df['SubType'] != 2)]
        df = df.sort_values(['Thk', 'Wid', 'SubPartLen', 'Wt', 'SubPartNo'],
                            ascending=[False, False, False, False, True])
        df['Sum_Qty'] = df.groupby(['SubPartNo'])['QtyPSeq'].transform('sum')
        df.to_excel(self.writer, startrow=6, index=False, sheet_name='NWF Seq')
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['NWF Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = ''
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if str(row['SubPartNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = str(row['SubPartNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6, sheet_name='NWF Raw')

    def xls_report_no_web_flange_batch(self, batch_to_batch):
        start_stack_no = int(batch_to_batch[0])
        end_stack_no = int(batch_to_batch[1])
        df = pd.DataFrame(self.get_all_list(), columns=self.pd_heads)
        df = df.loc[(df['SubType'] != 1) & (df['SubType'] != 2)
                    & (start_stack_no <= df['StackNo']) & (df['StackNo'] <= end_stack_no)]
        df = df.sort_values(['Thk', 'Wid', 'SubPartLen', 'Wt', 'SubPartNo'],
                            ascending=[False, False, False, False, True])
        df['Sum_Qty'] = df.groupby(['SubPartNo'])['QtyPSeq'].transform('sum')
        df.to_excel(self.writer, startrow=6, index=False,
                    sheet_name=('NWF ' + str(batch_to_batch[0]) + '-' + str(batch_to_batch[1]) + ' Seq'))
        number_rows_all = len(df.index)
        if number_rows_all > 0:
            workbook = self.writer.book
            format_body = workbook.add_format({'bg_color': '#FFC7CE'})
            format_number = workbook.add_format({'num_format': '#,##0.00'})
            worksheet = self.writer.sheets['NWF ' + str(batch_to_batch[0]) + '-' + str(batch_to_batch[1]) + ' Seq']
            cell_range = 'C7:H' + str(number_rows_all + 7)
            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format_body})
            worksheet.set_column('J8:K' + str(number_rows_all + 7), 9, format_number)

            format_top_border = workbook.add_format()
            format_top_border.set_top()
            old_value = ''
            row_fix = 6
            for index, row in df.iterrows():
                row_fix += 1
                if str(row['SubPartNo']) != old_value:
                    worksheet.set_row(row_fix, None, format_top_border)
                    old_value = str(row['SubPartNo'])

            df_raw = df.groupby(['Thk', 'Wid'])['WtPSeq', 'SubPartLenPSeq'].sum()  # 生成的是series
            df_raw.to_excel(self.writer, startrow=6,
                            sheet_name=('NWF ' + str(batch_to_batch[0]) + '-' + str(batch_to_batch[1]) + ' Raw'))

    def all_report(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if self.batch_state == 2:
            if not self.batch_c.stacks:
                self.show_info('Error', 'You have not records. \n Batching first, please!')
            else:
                all_list = self.get_all_list()
                try:
                    df = pd.DataFrame(all_list, columns=self.pd_heads)
                    create_date = "{:%m-%d-%Y}".format(date.today())
                    create_by = self.user_account
                    work_depart = 'All'
                    footer = [('Create By', [create_by]), ('Creat Date', [create_date]), ('Version', [0.1]),
                              ('Weight Unit', ['kg']), ('Length Unit', ['mm'])]
                    header = [('Orders', [self.orders]), ('Department', [work_depart])]
                    df_footer = pd.DataFrame.from_items(footer)
                    df_header = pd.DataFrame.from_items(header)
                    # print(self.orders[0])
                    writer = pd.ExcelWriter(self.orders[0] + '_' + work_depart + '.xlsx', engine='xlsxwriter')
                    df.to_excel(writer, startrow=6, index=False, freeze_panes=[7, 0])
                    df_footer.to_excel(writer, index=False)
                    df_header.to_excel(writer, startrow=3, index=False)
                except Exception as e:
                    print(e)
                finally:
                    self.writer.save()
                    self.statusBar.showMessage('Report file has been saved, take it in the root fold of this program!')
                    self.show_info('info', 'File saved!')

        if self.batch_state == 3:
            if not self.batch_c.stacks:
                self.show_info('Error', 'You have not records. \n Batching first, please!')
            else:
                try:
                    out_path = QFileDialog.getExistingDirectory()
                    out_path = out_path + '\\' + self.orders[0] + '_' + 'All.xlsx'
                    self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                    if self.lineEdit_Batch_the_Batch.text() == '':
                        # print('is not none')
                        self.xls_report_no_web_flange()
                        self.xls_report_header('NWF')
                    else:
                        # print(self.lineEdit_Batch_the_Batch.text())
                        batch_the_batch = self.lineEdit_Batch_the_Batch.text()
                        batch_the_batch = re.split(u';|；|\s|\s*', batch_the_batch)
                        for item in batch_the_batch:
                            item_batch = re.split(u'-', item)
                            self.xls_report_no_web_flange_batch(item_batch)
                            self.xls_report_header('NWF ' + item_batch[0] + '-' + item_batch[1])
                    self.xls_report_plan()
                    self.xls_report_header('Plan')

                    self.xls_report_all()
                    self.xls_report_header('All')
                    self.xls_report_flange()
                    self.xls_report_header('Flange')
                    self.xls_report_web()
                    self.xls_report_header('Web')
                    self.xls_report_stiff()
                    self.xls_report_header('Stiff')
                    self.xls_report_clip()
                    self.xls_report_header('Clip')
                    self.xls_report_plate()
                    self.xls_report_header('Plate')
                    self.xls_report_burn()
                    self.xls_report_header('Burn')
                    self.xls_report_man_hour()
                    self.xls_report_header('Man_hour')

                except Exception as e:
                    # self.show_info('info', 'File saved!')
                    self.show_info('Error', e)
                    print(e)
                finally:
                    self.format_excel()
                    self.writer.save()
                    self.show_info('info', 'File saved!')
                    return

    def flange_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'flange.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_flange()
                self.xls_report_header('Flange')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def web_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'web.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_web()
                self.xls_report_header('Web')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def stiff_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'stiff.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_stiff()
                self.xls_report_header('Stiff')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def clip_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'clip.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_clip()
                self.xls_report_header('Clip')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def plate_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'plate.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_plate()
                self.xls_report_header('Plate')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def burn_report(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        if not self.batch_c.stacks:
            self.show_info('Error', 'You have not records. \n Batching first, please!')
        else:
            try:
                out_path = QFileDialog.getExistingDirectory()
                out_path = out_path + '\\' + self.orders[0] + '_' + 'burn.xlsx'
                self.writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
                self.xls_report_burn()
                self.xls_report_header('Burn')
            except Exception as e:
                # self.show_info('info', 'File saved!')
                self.show_info('Error', e)
                print(e)
            finally:
                self.format_excel()
                self.writer.save()
                self.show_info('info', 'File saved!')
                return

    def web_view(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        self.report_stack_web.stack_all = []
        self.report_stack_web.stack_all = self.batch_c.stacks
        self.report_stack_web.set_table()
        self.report_stack_web.show()

    def flange_view(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_flange.stack_all = []
        self.report_stack_flange.stack_all = self.batch_c.stacks
        self.report_stack_flange.set_table()
        self.report_stack_flange.show()

    def plate_view(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_plate.stack_all = []
        self.report_stack_plate.stack_all = self.batch_c.stacks
        self.report_stack_plate.set_table()
        self.report_stack_plate.show()

    def clip_view(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_clip.stack_all = []
        self.report_stack_clip.stack_all = self.batch_c.stacks
        self.report_stack_clip.set_table()
        self.report_stack_clip.show()

    def burn_view(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_burn.stack_all = []
        self.report_stack_burn.stack_all = self.batch_c.stacks
        self.report_stack_burn.set_table()
        self.report_stack_burn.show()

    def stiff_view(self):
        if self.batch_state < 3:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_stiff.stack_all = []
        self.report_stack_stiff.stack_all = self.batch_c.stacks
        self.report_stack_stiff.set_table()
        self.report_stack_stiff.show()

    def report_stack_with_subparts(self):
        if self.batch_state < 2:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        # self.show_info('information', 'I am here!')
        self.report_with_subparts.stack_all = []
        self.report_with_subparts.stack_all = self.batch_c.stacks
        self.report_with_subparts.set_table()
        self.report_with_subparts.show()

    def nc_deal(self):
        if self.batch_state < 2:
            self.statusBar.showMessage('Error: You must run pre step first!')
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        try:
            my_sub_parts = []
            my_parts = []
            text = self.lineEdit_nc_path.text()
            if text == '':
                self.show_info('Error', 'You haven\'t select the NC Path! \\n Please select the NC Path...')
                self.lineEdit_nc_path.setFocus()
            else:
                self.nc_file_path = text
                if self.orders:
                    for my_part in self.batch_c.stacks:
                        # pprint(my_part)
                        my_parts.append(my_part[2])
                        for one_part in my_part[2].subparts:
                            # pprint(one_part)
                            if one_part[0] in my_sub_parts:
                                # self.show_info('info', 'i am here')
                                pass
                            else:
                                # self.show_info('info', sub_part[0].no)
                                my_sub_parts.append(one_part[0])

                    if self.nc_file_path != '':
                        for sub_part in my_sub_parts:
                            nc_file_with_path = self.nc_file_path + '/' + sub_part.no.split('-')[0] + '.nc1'
                            # print(nc_file_with_path)
                            if is_exist_nc(nc_file_with_path):
                                dia = has_hole_nc(nc_file_with_path)
                                sub_part.get_holes_dia(dia)
                            sub_part.get_subpart_type()

                    for my_part in my_parts:
                        my_part.get_man_hour_hw()

                    self.create_out_fold()
                    self.flange_nc_to_fmi()
                    self.flange_nc_to_ped()

                    self.show_info('Finish Read NC', 'I have finished reading NC Files!')
                    self.batch_state = 3
                    self.statusBar.showMessage('Next: Finished add NC information! Get your report!')
                else:
                    self.statusBar.showMessage('Error: You should run Batching First!')
                    self.show_info('Error', 'You have\'t Bathing! \\n Please run Batching First...')
        except error:
            print(strerror(error.errno))

    def browse_nc_path(self):
        self.lineEdit_nc_path.setText(QFileDialog.getExistingDirectory(None, 'Please Indicate a NC fold:'))

    def report_stack_total(self):
        if self.batch_state < 1:
            self.show_info('Error', 'Pre_Step have not been finished!')
            return

        self.report_stack_form.stack_all = []
        self.report_stack_form.stack_all = self.batch_c.stacks
        self.report_stack_form.set_table()
        # self.show_info('info', 'I am here!')
        self.report_stack_form.show()
        # pass

    def show_info(self, title, context):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        title,
                                        context,  # + str(self.pass_info),
                                        QMessageBox.Ok)
        return reply

    def get_batch(self):
        self.get_orders()
        self.statusBar.showMessage('Message: You selected-- ' + self.orders[0])

        orders_b = []
        if self.batch_state < 1:
            self.statusBar.showMessage('Error: You must finished the pre Step first!')
            self.show_info('Error', 'Pre_Step have not been finished!')
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.statusBar.showMessage('Message: Now Batching! ' + self.orders[0] + ' Please Wait a moment...')
        self.orders = self.tableWidget_orders.selected_orders
        # -----需要修改
        # -----获取orders的列表
        orders_b = self.tableWidget_orders.selected_orders[::4]
        # print(orders_b)

        # orders_b = [self.orders[0]]

        self.batch_c.no = 1  # ------------------batch no ------------
        for order_n in orders_b:
            order_c = c_set_order(order_n, self.db)
            self.batch_c.get_orders(order_c)
            self.batch_c.quantity += order_c.quantity
            self.batch_c.weight += order_c.weight
            self.batch_c.orders_quantity += 1
            self.batch_c.get_batch_parts()
            self.batch_c.sort_by_flange()
            self.batch_c.sort_by_web()
            web_flange = self.by_web_or_flange
        self.batch_c.sum_area()
        # print('by_web_or_flange', self.by_web_or_flange, '--', self.limit_flange_wt, '---', self.limit_web_wt)
        # print(self.batch_c.order_parts_f)
        # print('---------------------')
        # print(self.batch_c.order_parts_w)
        self.batch_c.batching(web_flange, self.limit_flange_wt, self.limit_web_wt)
        # if 0 == self.by_web_or_flange:  # by web
        #     print('by_web_ing')
        #     self.batch_c.sort_by_web()
        #     self.batch_c.batching(0, self.limit_flange_wt, self.limit_web_wt)
        # else:
        #     print('by_flange_ing')
        #     self.batch_c.sort_by_flange()
        #     self.batch_c.batching(1, self.limit_flange_wt, self.limit_web_wt)
        QApplication.restoreOverrideCursor()
        self.batch_state = 2
        self.statusBar.showMessage('Next: Finished Batch! Please Select the NC file folder!' + self.orders[0])
        self.show_info('Finish', 'Finish batching')

    def show_orders(self):
        self.get_all_orders()
        self.tableWidget_orders.all_order = self.all_order
        self.tableWidget_orders.set_table()
        self.tableWidget_orders.show()
        self.get_orders()

        self.repaint()
        self.statusBar.showMessage('Message: You have selected the Orders: ' + str(self.orders))

    def get_orders(self):
        self.orders = self.tableWidget_orders.selected_orders
        if self.orders:
            self.batch_state = 1

    def login(self):
        self.loginD.show()
        # self.loginD.pushButton.clicked.connect(self.get_user_info)

    def get_user_info(self):

        self.user_info = self.loginD.pass_info
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        self.by_web_or_flange = int(cf.get('by_web_or_flange', 'by_web_or_flange'))
        # print(self.by_web_or_flange)
        if self.user_info[0] != '':
            self.server = cf.get(self.user_info[0], 'server')
            self.database = cf.get(self.user_info[0], 'database')
            try:
                import pymssql
                conn = pymssql.connect(host=self.server, user=self.user_info[1], password=self.user_info[2],
                                       database=self.database, as_dict=True)
                conn.close()
                self.loginD.hide()
                QMessageBox.information(self,
                                        "Login Ok",
                                        "You login the database success! \n Now, welcome to batching...",
                                        QMessageBox.Ok)
            except Exception as e:

                # self.statusBar.showMessage(e)
                QMessageBox.information(self,
                                        "Login Error",
                                        "Can not Login the Database, \ncheck the network and user account/password!",
                                        QMessageBox.Ok)
                self.loginD.show()
                self.show()
                return
            finally:

                # self.show()
                return
        else:
            self.show_info('Error', 'Please select your site!')
            self.login()

    def get_all_orders(self):
        self.db = DBUnit(str(self.user_info[1]), str(self.user_info[2]), main_show.server, main_show.database)
        # print('i am here')
        self.all_order = c_get_all_orders(self.db)

    def set_nc_path(self, nc_path):
        self.nc_path = nc_path  # 'E:\Zanweb\PythonProgram\Batch\爱仕达11#NC文件\\'
        return nc_path


if __name__ == '__main__':
    # from bclass import *
    # from bfunc import *
    from dbunit import *
    from bc_read import *
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_show = MainWindow()
    main_show.show()
    main_show.loginD.show()

    sys.exit(app.exec_())

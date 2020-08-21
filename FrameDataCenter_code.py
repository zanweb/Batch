#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2019/12/1 21:52
# @Author   :   ZANWEB
# @File     :   FrameDataCenter_code.py in Batch
# @IDE      :   PyCharm

import sys
from itertools import groupby
from operator import itemgetter

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem

from FrameDataCenter import Ui_MainWindow
from dbunit import DBUnit
from Frame_Data_Center_Functions import *

from GUI.Query88 import Query


class UiMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # self.showMaximized()
        self.user_info = {'server': '', 'database': '', 'account': '', 'password': ''}
        # self.tab3 = Query()
        self.tab3 = None
        self.push_button.setText('查询88')

    def ui_set(self):
        self.setWindowTitle(
            '钢构数据中心登录:' + str(self.user_info['server']) + '::' + str(self.user_info['database']) + '::' + str(
                self.user_info['account']))

        self.create_function_tree()
        self.tree_widget_function_tree.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.get_tree_view_function)
        self.groupBox.close()

    def get_role_tree_user_name(self, user_name):
        sql = "SELECT [dbo].[tblMainTree].[NodeID] \
      ,[Descp] \
      ,[ParentID] \
      ,[FormName] \
      ,[Upts] \
      ,[AutoNo] \
  FROM [MfgmisCSSQL].[dbo].[tblMainTree] INNER JOIN [dbo].[tblMaintreeRight] \
  ON [dbo].[tblMainTree].[NodeID] = [dbo].[tblMaintreeRight].[NodeID] \
  WHERE [dbo].[tblMaintreeRight].[RolerID] = (SELECT [RolerID] FROM [dbo].[tblUser] WHERE [UserName] = '" + user_name + "')"
        db = DBUnit(self.user_info['account'], self.user_info['password'], self.user_info['server'],
                    self.user_info['database'])
        rs = db.read(sql)
        return rs

    def set_tree_view_function(self, rs_data):
        self.tree_widget_function_tree.clear()
        self.tree_widget_function_tree.headerItem().setText(0, '功能树---BlueScope Frame Data Center')
        root = QTreeWidgetItem(self.tree_widget_function_tree)
        root.setText(0, '钢构车间管理系统')

        tree_group = []
        rs_data.sort(key=itemgetter('NodeID'))
        for index, group_items in groupby(rs_data, key=itemgetter('ParentID')):
            tree_group.append([index, list(group_items)])
        first_element = None
        for index, group_items in tree_group:
            if index == 0:
                first_element = group_items
                break
        self.tree_view_add_items(0, root, first_element, tree_group)
        self.tree_widget_function_tree.expandAll()

        return

    def tree_view_add_items(self, parent_id, parent, element, tree_group):
        for item in element:
            if item['NodeID'] != 0:
                child_item = QTreeWidgetItem()
                child_item.setText(0, str(item['Descp']))
                child_item.setCheckState(0, Qt.Unchecked)
                for index, group_items in tree_group:
                    if index == item['NodeID']:
                        self.tree_view_add_items(item['NodeID'], child_item, group_items, tree_group)
                        # break
                parent.addChild(child_item)
                # self.tree_view_add_items(index, parent, group_items)

    def create_function_tree(self):
        tree_data = []
        tree_data = self.get_role_tree_user_name(self.user_info['account'])
        # print(tree_data)
        self.set_tree_view_function(tree_data)

    @pyqtSlot(QTreeWidgetItem, int)
    def get_tree_view_function(self, item, column):
        # item_get = self.tree_widget_function_tree.selectedItems()
        item_get = item.text(column)
        select_functions(item_get, self)

    @pyqtSlot()
    def on_push_button_clicked(self):
        self.tab3 = Query()

        self.tabWidget.clear()
        self.tabWidget.tabPosition()
        self.tabWidget.addTab(self.tab3, '查询88')
        self.tab3.get_user_info(self.user_info)

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UiMain()
    window.show()
    sys.exit(app.exec_())

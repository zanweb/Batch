import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QComboBox, \
    QFrame, QMenu, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QColor, QBrush, QPixmap, QCursor
# from dbunit import *
# from bc_read import *


class AllOrders(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.all_order = []
        self.selected_orders = []
        self.table = QTableWidget()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.table.customContextMenuRequested[QPoint].connect(self.show_context_menu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.searchBox = QLineEdit()
        self.searchLabel = QLabel()
        self.searchButton = QPushButton('Search', self)
        self.searchButton.clicked.connect(self.search_order)

    def init_ui(self):
        self.setGeometry(300, 300, 700, 300)

    def set_table(self):
        horizontalHeader = ["OrderNo", "DescName", "TtlQty", "TtlWt"]
        self.setWindowTitle('All Orders')

        self.table.setColumnCount(4)
        self.table.setRowCount(2)
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.selectionModel().selectedRows()
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        # 自动调整列宽
        # self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        # self.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)

        for index, one in enumerate(self.all_order):
            self.table.setItem(index, 0, QTableWidgetItem(one['ProjID']))
            self.table.setItem(index, 1, QTableWidgetItem(one['ProjName']))
            self.table.setItem(index, 2, QTableWidgetItem(str(int(one['TtlQty'])) if one['TtlQty'] is not None else ''))
            self.table.setItem(index, 3, QTableWidgetItem(str(int(one['TtlWt']*1000)/1000) if one['TtlWt'] is not None else ''))
            # print(one['TtlQty'])
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)

        self.table.resizeColumnsToContents()
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.searchLabel.setText("Please Enter the Order for search:")
        self.searchButton.setMaximumSize(100, 50)
        mainLayout = QVBoxLayout()
        # searchLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        mainLayout.addWidget(self.searchLabel)
        mainLayout.addWidget(self.searchBox)
        mainLayout.addWidget(self.searchButton)

        # mainLayout.addWidget(searchLayout)
        self.setLayout(mainLayout)

    def get_selected_items(self):
        self.selected_orders = []
        # indexes = self.table.selectionModel().selectedRows()
        # rows = []
        # for indx in self.table.selectedIndexes():
        #     rows.append(indx.row)
        # try:
        #     print(QTableWidget.item(indx, 0).text())
        # except Exception as e:
        #     print(e)

        items = self.table.selectedItems()
        item_count = len(items)
        # print('item count', item_count)
        if item_count <= 0:
            pass
            # return 0
        else:
            for item in items:
                self.selected_orders.append(item.text())

        # self.selected_orders.append(items.text())
        # print(self.selected_orders)
        # return self.selected_orders

    def show_context_menu(self, event):
        # # self.table.exec_(QCursor.pos())
        self.table.contextMenu = QMenu(self)
        self.table.contextMenu.popup(QCursor.pos())
        action1 = self.table.contextMenu.addAction('Select and Exit', self.select_exit)
        action1.triggered.connect(self.select_exit)
        self.table.contextMenu.show()
        # print('open ok')
        # return self.table.contextMenuEvent(self, event)

    def select_exit(self):
        self.get_selected_items()
        # print('select')
        # print(self.selected_orders)

        self.hide()

    def search_order(self):
        items = self.table.findItems(self.searchBox.text(), Qt.MatchExactly)
        if items:
            item_row = (item.row() + 1 for item in items)
            self.table.scrollToItem(items[0])
            self.table.verticalScrollBar().setSliderPosition(items[0].row())
        else:
            msg_box = QMessageBox()
            msg_box.setText("Can't find your Order!")
            msg_box.exec()

    # def close_event(self, Event):
    #     pass
    #     # print('close even captured')


if __name__ == '__main__':
    from dbunit import *
    from bc_read import *

    # db = DBUnit('sa', 'zanweb5186', '127.0.0.1\zanwebsql', 'MFGMISCSSQL')
    db = DBUnit('frame', '123456', 'btint4', 'MFGMISCSSQL')

    all_order = c_get_all_orders(db)
    # print(all_order[0])
    app = QApplication(sys.argv)
    table = AllOrders()
    table.all_order = all_order
    table.set_table()
    table.baseSize()
    table.show()
    sys.exit(app.exec_())
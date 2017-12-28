from bc_read import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QApplication


class StackAll(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.table = QTableWidget()
        self.stack_all = []

    def init_ui(self):
        # form_report_stack_total.setObjectName("form_report_stack_total")
        # form_report_stack_total.resize(600, 300)
        self.setGeometry(300, 300, 1200, 300)

    def set_table(self):
        horizontalHeader = ["stack", "sequence", "parts", "length", 'Qty', 'WebThk', 'WebWid', 'WebWt', 'FlangeThk'
                            , 'FlangeWid', 'FlangeWt', 'PartWts']
        self.setWindowTitle('All stacks')
        self.table.setColumnCount(12)
        self.table.setRowCount(1)
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.selectionModel().selectedRows()
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)

        for index, stack in enumerate(self.stack_all):
            self.table.setItem(index, 0, QTableWidgetItem(str(stack[0])))
            self.table.setItem(index, 1, QTableWidgetItem(str(stack[1])))
            self.table.setItem(index, 2, QTableWidgetItem(stack[2].no))
            self.table.setItem(index, 3, QTableWidgetItem(str(stack[2].len)))
            self.table.setItem(index, 4, QTableWidgetItem(str(int(stack[3]))))
            self.table.setItem(index, 5, QTableWidgetItem(str(stack[2].web[0].thk)))
            self.table.setItem(index, 6, QTableWidgetItem(str(stack[2].web[0].wid)))
            self.table.setItem(index, 7, QTableWidgetItem(str(int(stack[2].web_wt * stack[3]*1000)/1000)))
            self.table.setItem(index, 8, QTableWidgetItem(str(stack[2].flange[0].thk)))
            self.table.setItem(index, 9, QTableWidgetItem(str(stack[2].flange[0].wid)))
            self.table.setItem(index, 10, QTableWidgetItem(str(int(stack[2].flange_wt * stack[3]*1000)/1000)))
            self.table.setItem(index, 11, QTableWidgetItem(str(int(stack[2].wt * stack[3]*1000)/1000)))
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)

        self.table.resizeColumnsToContents()
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    from dbunit import *
    from bfunc import *
    from bclass import *
    from pprint import pprint
    from os import *
    import sys

    from operator import itemgetter, attrgetter

    from time import time

    start = datetime.datetime.now()

    db = DBUnit('sa', 'zanweb5186', '127.0.0.1\zanwebsql', 'MFGMISCSSQL')
    orders = ['1602043801-2221-001C']

    all_orders = c_get_all_orders(db)
    # pprint(all_orders)  # 所有订单

    batch_b = BATCH()
    batch_b.no = 1

    for order_name in orders:
        order = c_set_order(order_name, db)
        batch_b.get_orders(order)
        batch_b.quantity += order.quantity
        batch_b.weight += order.weight
        batch_b.orders_quantity += 1

        batch_b.get_batch_parts()

    # pprint(batch.batch_parts)

    batch_b.sort_by_flange()

    # for part in batch.order_parts_f:
    #     print(part[0].no, '-'*5, part[0].len, '-'*5, part[1], '-'*5, part[0].flange[0].thk, '-'*5,
    #           part[0].flange[0].wid, '-'*5, part[0].flange[0].wt, '-'*5, part[0].flange_wt,
    #           '-'*5, part[0].web[0].thk, '-'*5, part[0].web[0].wid, '-'*5, part[0].web[0].wt,
    #           '-'*5, part[0].web_wt, '-'*5, part[2])

    batch_b.batching(1)  # by web
    pprint(batch_b.stacks)
    end = datetime.datetime.now()
    a = end - start
    print('time using:', a.seconds)
    app = QApplication(sys.argv)
    table = StackAll()
    table.stack_all = batch_b.stacks
    table.set_table()
    table.baseSize()
    table.show()
    sys.exit(app.exec_())
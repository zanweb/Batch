from bfunc import *
from bclass import *
from dbunit import *
from nc import *

# from main_window_code import *

# db = DBUnit(MainWindow.user_info[2], MainWindow.user_info[3], MainWindow.server, MainWindow.database)

# db = DBUnit('zyq2', 'zyq2', 'stlsojsvr04', 'MFGMISCSSQL')


def c_get_all_orders(db):
    sql = get_all_orders()
    rs = db.read(sql)
    return rs


def c_get_subpart_detail(subpart_no, subpart_len, db):
    sql = c_subpart_detail(subpart_no, subpart_len)
    rs = db.read(sql)
    return rs


def c_get_part_detail(part_no, part_len, db):
    sql = c_part_detail(part_no, part_len)
    rs = db.read(sql)
    return rs


def c_get_order_detail(order_no, db):
    sql = c_order_detail(order_no)
    rs = db.read(sql)
    return rs


def c_get_order_parts(order_no, db):
    sql = c_order_parts_detail(order_no)
    rs = db.read(sql)
    return rs


def c_get_part_subparts(part_no, part_len, db):
    sql = c_part_subparts(part_no, part_len)
    rs = db.read(sql)
    # print(sql)
    return rs


def c_set_part(part_no, part_len, db):
    # 构件
    part = c_get_part_detail(part_no, int(part_len), db)

    c_part = PART()
    c_part.no = part[0]['PrtNo'].strip() if part[0]['PrtNo'] else ''
    c_part.len = part[0]['Len']
    c_part.wid = part[0]['Wid']
    c_part.web_thk = part[0]['WebThk']
    c_part.flange_thk = part[0]['FlangeThk']
    c_part.dec = part[0]['Descp'].strip() if part[0]['Descp'] else ''
    c_part.high = part[0]['High']
    c_part.end_plate_qty = part[0]['EndPlateQty']
    c_part.stiff_qty = part[0]['StiffQty']
    c_part.full_weld_qty = part[0]['FullStiffQty']
    c_part.is_double_weld = part[0]['IsDWeld']
    c_part.is_change_sec = part[0]['IsChgSec']
    c_part.weld_foot = part[0]['WeldFoot']
    c_part.is_full_weld = part[0]['IsFullWeld']
    c_part.second_web = part[0]['No2Web'].strip() if part[0]['No2Web'] else ''
    c_part.second_flange = part[0]['No2Flange'].strip() if part[0]['No2Flange'] else ''
    c_part.part_type = part[0]['PrtTypeID']

    part_subparts = c_get_part_subparts(c_part.no, c_part.len, db)
    for subpart in part_subparts:
        # print(subpart['SubPrtNo'], int(subpart['SubPrtLen']))
        c_subpart = c_set_subpart(subpart['SubPrtNo'].strip(), int(subpart['SubPrtLen']), db)
        c_part.get_subpart(c_subpart, subpart['Qty'])
    c_part.main_web()
    c_part.main_flange()
    c_part.sum_part_wt()
    c_part.sum_area()
    c_part.get_man_hour_hw()
    return c_part


def c_set_subpart(subpart_no, subpart_len, db):
    # 零件
    sub_part = c_get_subpart_detail(subpart_no, subpart_len, db)
    # print(sub_part)  # 打印零件
    c_sub_part = SUBPART()

    c_sub_part.len = int(sub_part[0]['Len'])
    c_sub_part.no = sub_part[0]['SubPrtNo'].strip()
    c_sub_part.dec = sub_part[0]['Descp'].strip().upper()
    c_sub_part.thk = float(sub_part[0]['Thk'])
    c_sub_part.wid = float(sub_part[0]['Wid'])
    c_sub_part.wt = float(sub_part[0]['Wt'])
    c_sub_part.isd = sub_part[0]['IsDetail']
    c_sub_part.get_area()
    c_sub_part.get_perimeter()
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    # file_with_path = file_with_path + c_sub_part.no.split('-')[0]
    # if is_exist_nc(file_with_path):
    #     c_sub_part.get_holes_dia()
    # c_sub_part.get_area()  # 计算零件面积
    # c_sub_part.get_perimeter()  # 计算零件周长
    # print(c_sub_part.area)  # 打印零件面积
    return c_sub_part


def c_set_order(order_no, db):
    order = c_get_order_detail(order_no, db)
    # pprint(order)
    c_order = ORDER()
    c_order.no = order[0]['ProjID']
    c_order.name = order[0]['ProjName']
    c_order.weight = float(order[0]['TtlWt'])
    c_order.quantity = float(order[0]['TtlQty'])
    c_order.order_lines = 0

    # pprint(c_order.name)  # 打印订单名称

    order_parts = c_get_order_parts(c_order.no, db)

    for parts_line in order_parts:
        # 构件
        c_part = c_set_part(parts_line['TPNo'], int(parts_line['Len']), db)
        c_order.get_parts(c_part, parts_line['Qty'])

    # print(c_order.parts[0][0].no, c_order.parts[0][0].len, c_order.parts[0][1])
    c_order.sum_area()

    return c_order


def c_set_batch(orders):
    pass


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

    #db = DBUnit('sa', 'zanweb5186', '127.0.0.1\zanwebsql', 'MFGMISCSSQL')
    db = DBUnit('frame', '123456', 'btint4', 'MFGMISCSSQL')
    orders = ['1701008101-2211-002C']
    # orders = ['1600198501-2231-002C']
    file_with_path = 'E:\Zanweb\PythonProgram\Batch\爱仕达11#NC文件\\'

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

    batch_b.sort_by_web()

    # for part in batch.order_parts_f:
    #     print(part[0].no, '-'*5, part[0].len, '-'*5, part[1], '-'*5, part[0].flange[0].thk, '-'*5,
    #           part[0].flange[0].wid, '-'*5, part[0].flange[0].wt, '-'*5, part[0].flange_wt,
    #           '-'*5, part[0].web[0].thk, '-'*5, part[0].web[0].wid, '-'*5, part[0].web[0].wt,
    #           '-'*5, part[0].web_wt, '-'*5, part[2])

    batch_b.batching(0, 4500, 4500)  # by web
    pprint(batch_b.stacks)
    end = datetime.datetime.now()
    a = end - start
    print('time using:', a.seconds)

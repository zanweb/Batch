# import pymssql
from dbunit import *
from bfunc import *
# import time
from pprint import pprint

a = time.time()
db = DBUnit('zyq2', 'zyq2', 'stlsojsvr04', 'MFGMISCSSQL')  # 不使用默认端口

# orders = ['1602283601-2211-006C', '1602043801-2221-001C', '1602283601-2211-004C']
orders = ['1602283601-2211-006C']
sort_w = '%WEB%'
sort_f = '%FLANGE%'

sql = "select t.* from(SELECT  tblManifestTP.ProjID, tblPrtAssm.PrtNo AS PartNO," \
      " tblPrtAssm.PrtLen AS PartLength, tblManifestTP.Qty AS PartQty, tblPrtAssm.SubPrtNo,  tblSubPrt.Thk," \
      " tblSubPrt.Wid, tblSubPrt.Len,  tblSubPrt.Descp,  " \
      " ROW_NUMBER() OVER(partition by dbo.tblPrtAssm.PrtNo, dbo.tblPrtAssm.PrtLen order by tblSubPrt.Thk DESC, " \
      " tblSubPrt.Wid DESC, tblSubPrt.Len DESC) rn" \
      " FROM  tblSubPrt INNER JOIN" \
      "   tblPrtAssm ON tblSubPrt.SubPrtNo = tblPrtAssm.SubPrtNo AND tblSubPrt.Len = tblPrtAssm.SubPrtLen INNER JOIN" \
      "       tblPrt ON tblPrtAssm.PrtNo = tblPrt.PrtNo AND tblPrtAssm.PrtLen = tblPrt.Len INNER JOIN" \
      "       tblManifestTP ON tblPrt.PrtNo = tblManifestTP.TPNo AND tblPrt.Len = tblManifestTP.Len" \
      " WHERE        (tblSubPrt.Descp LIKE '" + sort_w + "') AND " + select_orders(orders) + \
      " GROUP BY tblPrtAssm.PrtNo, tblPrtAssm.PrtLen, tblPrtAssm.SubPrtNo, tblPrtAssm.SubPrtLen, tblSubPrt.Thk," \
      " tblSubPrt.Wid, tblSubPrt.Len, tblSubPrt.Descp, tblManifestTP.ProjID, tblManifestTP.Qty) AS t" \
      " WHERE rn=1" \
      " ORDER BY t.Thk DESC, t.Wid DESC, t.Len DESC"

rs = db.read(sql)
sequence = 0
stack = 0
stacks = []

limit_flange_wt = 4500.0
limit_web_wt = 4500.0
limit_part_len = 3000

sum_flange_wt = 0.0
sum_web_wt = 0.0
flange_wt = 0.0
web_wt = 0.0
temp_qty = 0
stack_qty = 0
flange_wid = 0.0
flange_thk = 0.0
new_flange_size = ''
old_flange_size = ''

for row in rs:
    # 数据准备
    flange_wt = 0
    web_wt = 0
    temp_qty = 0
    sequence += 1

    # print('\n', row['PartNO'], '*', row['PartLength'], '---', row['PartQty'])
    p_qty = row['PartQty']
    p_no = row['PartNO']
    p_len = row['PartLength']
    rs_flange = db.read(get_subpart_flange(p_no, p_len))
    rs_web = db.read(get_subpart_web(p_no, p_len))

    # 计算flange_wt, web_wt
    for i in range(len(rs_flange)):
        flange_wt += rs_flange[i]['Wt'] * rs_flange[i]['Qty']
    for i in range(len(rs_web)):
        web_wt += rs_web[i]['Wt'] * rs_web[i]['Qty']

    # print(flange_wt, '----', web_wt)

    flange_thk = rs_flange[0]['Thk']
    flange_wid = rs_flange[0]['Wid']
    web_thk = rs_web[0]['Thk']
    web_wid = rs_web[0]['Wid']
    new_flange_size = str(flange_thk) + str(flange_wid)
    if new_flange_size != old_flange_size:
        stack += 1
        sum_flange_wt = 0
    # print(flange_thk, '*', flange_wid)
    # print('rest wt--------', sum_flange_wt, '-------------', sum_web_wt, '---------------')

    # 清理数据

    if (sum_flange_wt + flange_wt) > limit_flange_wt:   # 翼板堆重超
        if (sum_web_wt + web_wt) > limit_web_wt:            # 腹板堆重超
            sum_flange_wt = 0
            sum_web_wt = 0
            stack += 1
            # sequence += 1
        else:                                               # 腹板堆重不超
            sum_flange_wt = 0
            sum_web_wt += web_wt
            stack += 1
            # sequence += 1
    else:         # 翼板堆重不超    elif sum_flange_wt > limit_flange_wt * 0.5:
        if (sum_web_wt + web_wt) > limit_web_wt:            # 腹板堆重超
            # sum_flange_wt = 0
            sum_web_wt = 0
            # stack += 1
        else:                                               # 腹板堆重不超
            # sum_flange_wt = 0
            # sum_web_wt = 0
            # stack += 1
            pass

    # 读一组构件
    for pcs in range(p_qty):
        if limit_flange_wt >= (sum_flange_wt + flange_wt):  # 翼板堆重不超
            if limit_web_wt >= (sum_web_wt + web_wt):            # 腹板堆重不超
                temp_qty += 1
                sum_flange_wt += flange_wt
                sum_web_wt += web_wt
            else:  # 腹板堆重超
                print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                      flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-'*5,
                      temp_qty * flange_wt, '-'*5, temp_qty * web_wt)
                stack += 1
                sequence += 1
                sum_flange_wt += flange_wt
                sum_web_wt = web_wt
                temp_qty = 1
        else:                                          # 翼板堆重超
            if limit_web_wt >= (sum_web_wt + web_wt):       # 腹板堆重不超
                print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                      flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-'*5,
                      temp_qty * flange_wt, '-'*5, temp_qty * web_wt)
                stack += 1
                sequence += 1
                sum_flange_wt = flange_wt
                sum_web_wt += web_wt
                # print('flange ok++++++++web ok++++++++')
                temp_qty = 1
            else:                                           # 腹板堆重超
                print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                      flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-'*5,
                      temp_qty * flange_wt, '-'*5, temp_qty * web_wt)
                stack += 1
                sequence += 1
                sum_flange_wt = flange_wt
                sum_web_wt = web_wt
                # print('flange ok++++++++web ok++++++++')
                temp_qty = 1

    print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
          flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
          temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
    # print('+++++++++++++++++end of part type ++++++++++++++')
    old_flange_size = new_flange_size

print(a)

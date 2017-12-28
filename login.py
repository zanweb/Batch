# import pymssql
from dbunit import *
from bfunc import *
# import time
from pprint import pprint

a = time.time()
db = DBUnit('zyq2', 'zyq2', 'stlsojsvr04', 'MFGMISCSSQL')  # 不使用默认端口

# sql_org = "SELECT dbo.tblManifestTP.ProjID AS Manifest, dbo.tblManifestTP.TPNo AS PartNO,
# dbo.tblManifestTP.Qty AS PartQty, dbo.tblPrt.Wt AS PartUnitWeight, " \
#       "dbo.tblManifestTP.Len AS PartLength, dbo.tblPrt.Wid AS PartWidth,
# dbo.tblPrt.WebThk AS WebThickness, dbo.tblPrt.FlangeThk AS FlangeThickness," \
#       " dbo.tblPrtAssm.SubPrtNo AS SubpartNo, dbo.tblPrtAssm.SubPrtLen AS SubpartLenght,
# dbo.tblPrtAssm.Qty AS SubpartQtyInOnePart, " \
#       " dbo.tblSubPrt.Descp AS SubpartDescript, dbo.tblSubPrt.Thk AS SubpartThickness,
# dbo.tblSubPrt.Wid AS SubpartWidth, dbo.tblSubPrt.Wt AS SubpartWt" \
#       " FROM dbo.tblManifestTP INNER JOIN " \
#       " dbo.tblPrt ON dbo.tblManifestTP.Len = dbo.tblPrt.Len AND dbo.tblManifestTP.TPNo = dbo.tblPrt.PrtNo
# INNER JOIN" \
#       " dbo.tblPrtAssm ON dbo.tblPrt.PrtNo = dbo.tblPrtAssm.PrtNo AND dbo.tblPrt.Len = dbo.tblPrtAssm.PrtLen
# INNER JOIN" \
#       " dbo.tblSubPrt ON dbo.tblPrtAssm.SubPrtNo = dbo.tblSubPrt.SubPrtNo AND
# dbo.tblPrtAssm.SubPrtLen = dbo.tblSubPrt.Len" \
#       " WHERE (dbo.tblManifestTP.ProjID = N'1602283601-2211-006C')" \
#       " GROUP BY dbo.tblManifestTP.ProjID, dbo.tblManifestTP.TPNo, dbo.tblManifestTP.Qty,
# dbo.tblPrt.Wt, dbo.tblManifestTP.Len, dbo.tblPrt.Wid, dbo.tblPrt.WebThk," \
#       " dbo.tblPrt.FlangeThk, dbo.tblPrtAssm.SubPrtNo, dbo.tblPrtAssm.SubPrtLen, dbo.tblPrtAssm.Qty,
# dbo.tblSubPrt.Descp, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid," \
#       " dbo.tblSubPrt.Wt ORDER BY WebThickness DESC, FlangeThickness DESC"
# orders = ['1602283601-2211-006C', '1602043801-2221-001C']
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
      " WHERE        (tblSubPrt.Descp LIKE '" + sort_f + "') AND " + select_orders(orders) + \
      " GROUP BY tblPrtAssm.PrtNo, tblPrtAssm.PrtLen, tblPrtAssm.SubPrtNo, tblPrtAssm.SubPrtLen, tblSubPrt.Thk," \
      " tblSubPrt.Wid, tblSubPrt.Len, tblSubPrt.Descp, tblManifestTP.ProjID, tblManifestTP.Qty) AS t" \
      " WHERE rn=1" \
      " ORDER BY t.Thk DESC, t.Wid DESC, t.Len DESC"

rs = db.read(sql)
sequence = 0
stack = 1
stacks = []

limit_flange_wt = 3500.0
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
    # if rs_flange[0]['Thk'] != flange_thk or rs_flange[0]['Wid'] != flange_wid:
    #     sequence += 1
    flange_thk = rs_flange[0]['Thk']
    flange_wid = rs_flange[0]['Wid']
    web_thk = rs_web[0]['Thk']
    web_wid = rs_web[0]['Wid']
    # print(flange_thk, '*', flange_wid)
    # print('rest wt--------', sum_web_wt, '-------------', sum_flange_wt, '---------------')
    # 清理数据
    # if sum_flange_wt + flange_wt > limit_flange_wt or sum_flange_wt > limit_flange_wt * 0.5:
    #     sum_flange_wt = 0
    #     stack += 1
    # if sum_web_wt + web_wt > limit_web_wt or sum_web_wt > limit_web_wt * 0.5:
    #     sum_web_wt = 0
    #     # stack += 1
    #
    # if (sum_flange_wt + flange_wt > limit_flange_wt or sum_flange_wt > limit_flange_wt * 0.5) \
    #         and (sum_web_wt + web_wt > limit_web_wt or sum_web_wt > limit_web_wt * 0.5):
    #     sum_flange_wt = 0
    #     sum_web_wt = 0
    #     # stack += 1

    if ((sum_flange_wt + flange_wt) < limit_flange_wt) \
            and ((sum_web_wt + web_wt) < limit_web_wt):
        pass
    # if ((sum_flange_wt + flange_wt) < limit_flange_wt) and (sum_web_wt < (limit_web_wt * 0.5)):
    #     pass
    # if ((sum_web_wt + web_wt) < limit_web_wt) and (sum_flange_wt < (limit_flange_wt * 0.5)):
    #     pass
    # if ((sum_flange_wt + flange_wt) > limit_flange_wt) and (sum_web_wt < (limit_web_wt * 0.5)):
    #     sum_flange_wt = 0
    #     pass
    # if ((sum_web_wt + web_wt) > limit_web_wt) and (sum_flange_wt < (limit_flange_wt * 0.5)):
    #     sum_web_wt = 0
    #     pass
    else:
        sum_flange_wt = 0
        sum_web_wt = 0
        stack += 1

    # 写入stack

    for pcs in range(p_qty):
        if (limit_flange_wt >= (sum_flange_wt + flange_wt)) and (limit_web_wt >= (sum_web_wt + web_wt)):
            temp_qty += 1
            sum_flange_wt += flange_wt
            sum_web_wt += web_wt
            # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt,
            #       flange_wid, '*', flange_thk)
        elif (limit_web_wt < (sum_web_wt + web_wt)) and (limit_flange_wt < (sum_flange_wt + flange_wt)):

            stack += 1
            sequence += 1
            sum_flange_wt = flange_wt
            sum_web_wt = web_wt
            print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt,
                  flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid)
            # print('flange ok++++++++web ok++++++++')
            temp_qty = 1
        elif (limit_flange_wt < (sum_flange_wt + flange_wt)) and (limit_web_wt > (sum_web_wt + web_wt)):
            # pcs_to_stacks = {'stack': stack, 'sequence': sequence, 'PartNo': p_no, 'PartLength': p_len, 'PartQty':
            # temp_qty}

            print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt,
                  flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid)
            # print('flange ok++++++++++')
            stack += 1
            sequence += 1
            sum_web_wt += web_wt
            sum_flange_wt = flange_wt
            temp_qty = 1

        elif (limit_web_wt < (sum_web_wt + web_wt)) and (limit_flange_wt > (sum_flange_wt + flange_wt)):
            # pcs_to_stacks = {'stack': stack, 'sequence': sequence, 'PartNo': p_no, 'PartLength':
            #  p_len, 'PartQty': temp_qty}

            print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt,
                  flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid)
            # print('web ok++++++++++++++')
            stack += 1
            sequence += 1
            sum_web_wt = web_wt
            sum_flange_wt += flange_wt
            temp_qty = 1

    print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt,
          flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid)
    # print('+++++++++++++++++end of part type ++++++++++++++')



    # sequence += 1
    # print(temp_qty)
    # for pcs in p_qty:
    #
    #
    #     if sum_web_wt < limit_web_wt:
    #         pass
    #         if sum_flange_wt < limit_flange_wt:
    #             pass

    # for sub in rs_sub:
    #       print(sub)

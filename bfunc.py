def select_orders(orders_org):
    select_orders_sql = "') OR "
    orders = []
    for order in orders_org:
        orders.append("(dbo.tblManifestTP.ProjID = N'" + order)
    if len(orders) == 1:
        select_orders_sql = orders[0]
    if len(orders) > 1:
        select_orders_sql = select_orders_sql.join(orders)
    select_orders_sql = select_orders_sql + "')"
    return select_orders_sql


def get_subpart_all(part_no, part_length):
    sql = "SELECT dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.SubPrtNo, dbo.tblPrtAssm.SubPrtLen" \
          " FROM  dbo.tblPrtAssm INNER JOIN" \
          "       dbo.tblSubPrt ON dbo.tblPrtAssm.SubPrtNo = dbo.tblSubPrt.SubPrtNo AND dbo.tblPrtAssm.SubPrtLen = dbo.tblSubPrt.Len" \
          " WHERE (RTRIM(dbo.tblPrtAssm.PrtNo) = '" + part_no + "') AND (dbo.tblPrtAssm.PrtLen = " + str(
        part_length) + ")" \
                       " GROUP BY dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.PrtNo, dbo.tblPrtAssm.PrtLen, dbo.tblPrtAssm.SubPrtNo," \
                       "          dbo.tblPrtAssm.SubPrtLen"
    return sql


def get_subpart_fw(part_no, part_length):
    sql = "SELECT dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.SubPrtNo, dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp" \
          " FROM dbo.tblPrtAssm INNER JOIN" \
          "      dbo.tblSubPrt ON dbo.tblPrtAssm.SubPrtNo = dbo.tblSubPrt.SubPrtNo AND dbo.tblPrtAssm.SubPrtLen = dbo.tblSubPrt.Len " \
          " WHERE (dbo.tblPrtAssm.PrtLen = " + str(
        part_length) + ") AND (RTRIM(dbo.tblPrtAssm.PrtNo) = '" + part_no + "') AND ((UPPER(dbo.tblSubPrt.Descp) LIKE '%WEB%') OR" \
                                                                            "       (UPPER(dbo.tblSubPrt.Descp) LIKE '%FLANGE%'))" \
                                                                            " GROUP BY dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.PrtNo, dbo.tblPrtAssm.PrtLen, dbo.tblPrtAssm.SubPrtNo," \
                                                                            "          dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp"
    return sql


def get_subpart_flange(part_no, part_length):
    sql = "SELECT dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.SubPrtNo, dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp" \
          " FROM dbo.tblPrtAssm INNER JOIN" \
          "      dbo.tblSubPrt ON dbo.tblPrtAssm.SubPrtNo = dbo.tblSubPrt.SubPrtNo AND dbo.tblPrtAssm.SubPrtLen = dbo.tblSubPrt.Len " \
          " WHERE (dbo.tblPrtAssm.PrtLen = " + str(
        part_length) + ") AND (RTRIM(dbo.tblPrtAssm.PrtNo) = '" + part_no + "') AND " \
                                                                            "       (UPPER(dbo.tblSubPrt.Descp) LIKE '%FLANGE%')" \
                                                                            " GROUP BY dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.PrtNo, dbo.tblPrtAssm.PrtLen, dbo.tblPrtAssm.SubPrtNo," \
                                                                            "          dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp"
    return sql


def get_subpart_web(part_no, part_length):
    sql = "SELECT dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.SubPrtNo, dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp" \
          " FROM dbo.tblPrtAssm INNER JOIN" \
          "      dbo.tblSubPrt ON dbo.tblPrtAssm.SubPrtNo = dbo.tblSubPrt.SubPrtNo AND dbo.tblPrtAssm.SubPrtLen = dbo.tblSubPrt.Len " \
          " WHERE (dbo.tblPrtAssm.PrtLen = " + str(
        part_length) + ") AND (RTRIM(dbo.tblPrtAssm.PrtNo) = '" + part_no + "') AND " \
                                                                            "       (UPPER(dbo.tblSubPrt.Descp) LIKE '%WEB%')" \
                                                                            " GROUP BY dbo.tblPrtAssm.Qty, dbo.tblSubPrt.Thk, dbo.tblSubPrt.Wid, dbo.tblSubPrt.Wt, dbo.tblPrtAssm.PrtNo, dbo.tblPrtAssm.PrtLen, dbo.tblPrtAssm.SubPrtNo," \
                                                                            "          dbo.tblPrtAssm.SubPrtLen, dbo.tblSubPrt.Descp"
    return sql


def c_subpart_detail(subpart_no, subpart_len):
    sql = "SELECT * FROM dbo.tblSubprt WHERE RTRIM(dbo.tblSubprt.SubPrtNo)=N'" + subpart_no + "'" + " AND dbo.tblSubprt.Len=" + str(
        subpart_len)
    # print(sql)
    return sql


def c_part_detail(part_no, part_len):
    sql = "SELECT * FROM dbo.tblPrt WHERE RTRIM(dbo.tblPrt.PrtNo)=N'" + part_no + "'" + " AND dbo.tblPrt.Len=" + str(
        part_len)
    # print(sql)
    return sql


def c_order_detail(order_no):
    sql = "SELECT * FROM dbo.tblProj WHERE dbo.tblProj.ProjID=N'" + order_no + "'"
    # print(sql)
    return sql


def c_order_parts_detail(order_no):
    sql = "SELECT * FROM dbo.tblManifestTP WHERE dbo.tblManifestTP.ProjID=N'" + order_no + "'"
    # print(sql)
    return sql


def c_part_subparts(part_no, part_len):
    sql = "SELECT * FROM dbo.tblPrtAssm WHERE dbo.tblPrtAssm.PrtNo='" + part_no + "'" + " AND PrtLen=" + str(part_len)
    return sql


def get_all_orders():
    sql = "SELECT * FROM dbo.tblProj ORDER BY dbo.tblProj.ProjID DESC"
    return sql

if __name__ == '__main__':

    all_orders = get_all_orders()
    print(all_orders)

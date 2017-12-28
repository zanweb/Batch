class SUBPART:
    def __init__(self):
        self.no = ''
        self.len = 0.0
        self.wid = 0.0
        self.thk = 0.0
        self.dec = ''
        self.wt = 0.0
        self.isd = True
        self.perimeter = 0.0
        self.area = 0.0
        self.has_hole = False
        self.holes_dia = {}
        self.type = 0  # 0-undif, 1-web, 2-flange, 3-stiff, 4-clip, 5-burn/drill, 6-plate line
        # self.get_perimeter(self)
        # self.get_area(self)

    def get_perimeter(self):
        self.perimeter = 2 * (self.len + self.wid) / 1000
        return self.perimeter

    def get_area(self):
        self.area = self.len * self.wid / 1000000 * 2
        return self.area

    def get_holes_dia(self, holes_dia):
        if holes_dia:
            self.has_hole = True
            self.holes_dia = holes_dia

    def get_subpart_type(self):
        if self.dec.upper().find('WEB') != -1:
            self.type = 1
        elif self.dec.upper().find('FLANGE') != -1:
            self.type = 2
        elif not self.has_hole:
            self.type = 3
        elif self.thk < 16:
            self.type = 4
        elif 16 <= self.thk <= 30:
            if self.thk < min(self.holes_dia.keys()):
                self.type = 6
            else:
                self.type = 5
        else:
            self.type = 5


class PART:
    def __init__(self):
        self.no = ''
        self.len = 0.0
        self.wid = 0.0
        self.dec = ''
        self.high = 0.0
        self.web_thk = 0.0
        self.flange_thk = 0.0
        self.end_plate_qty = 0
        self.stiff_qty = 0
        self.full_weld_qty = 0
        self.is_double_weld = True
        self.is_change_sec = True
        self.weld_foot = 0.0
        self.is_full_weld = True
        self.second_web = ''
        self.second_flange = ''
        self.man_hour_hw = 0.0
        self.part_type = 0
        self.subparts = []
        self.web = SUBPART()
        self.flange = SUBPART()
        self.web_wt = 0.0
        self.flange_wt = 0.0
        self.wt = 0.0
        self.web_list = []
        self.flange_list = []
        self.stiff_list = []
        self.area = 0.0
        self.man_hour_line = 0.0
        self.man_hour_web = 0.0
        self.man_hour_flange = 0.0
        self.man_hour_plate = 0.0

    def get_subpart(self, subpart, qty):
        self.subparts.append([subpart, qty])

    def sum_area(self):
        for single in self.subparts:
            single_area = single[0].area * single[1]
            self.area += single_area

    def judge_subpart_type(self):  # move to subpart class
        pass

    def check_subpart(self):
        pass

    def main_web(self):
        # pass
        max_web_wt = 0.0
        t_web_wt = 0.0
        for web in self.subparts:
            if web[0].dec.upper().find('WEB') != -1:
                self.web_list.append([web[0], web[1]])
                t_web_wt += web[0].wt * web[1]
                if max_web_wt <= web[0].wt:
                    max_web_wt = web[0].wt * web[1]
                    self.web = web
        self.web_wt = t_web_wt

    def main_flange(self):
        max_flange_wt = 0.0
        t_flange_wt = 0.0
        for flange in self.subparts:
            if flange[0].dec.upper().find('FLANGE') != -1:
                self.flange_list.append([flange[0], flange[1]])
                t_flange_wt += flange[0].wt * flange[1]
                if max_flange_wt <= flange[0].wt:
                    max_flange_wt = flange[0].wt * flange[1]
                    self.flange = flange
        self.flange_wt = t_flange_wt

    def sum_part_wt(self):
        # single_total_wt = 0.0
        for single in self.subparts:
            single_wt = single[0].wt * single[1]
            self.wt += single_wt

    def get_man_hour_hw(self):
        # man_hour_hw
        full_weld = 1 if self.is_full_weld else 0
        double_weld = 1 if self.is_double_weld else 0
        weld_foot = self.weld_foot if self.weld_foot else 4
        end_plate_qty = self.end_plate_qty if self.end_plate_qty else 0
        stiff_qty = self.stiff_qty if self.stiff_qty else 0
        full_weld_qty = self.full_weld_qty if self.full_weld_qty else 0

        self.man_hour_hw = (0.75 + 0.05 * weld_foot) * (1 + 0.3 * double_weld) * (10 + 0.001 * self.len)
        self.man_hour_hw += end_plate_qty * (10 + 0.002 * self.wid) * (1.82 + 0.001 * self.high) * (0.76 + 0.02 * self.flange_thk) * (1 + 0.2 * full_weld)
        self.man_hour_hw += stiff_qty * (5 + 0.0015 * self.wid)
        self.man_hour_hw += (6 + 0.0005 * self.len) * (0.7 + 0.0005 * self.wid)
        self.man_hour_hw += full_weld_qty * 15

        # man_hour_line
        self.man_hour_line = self.len * 0.625 / 1000

        # man_hour_web
        # man_hour_flange
        # man_hour_plate
        for sub in self.subparts:
            if sub[0].dec.upper().find('WEB') != -1:
                self.man_hour_web += sub[0].perimeter / 3
            elif sub[0].dec.upper().find('FLANGE') != -1:
                self.man_hour_flange += sub[0].len / 10000
            else:
                self.man_hour_plate += sub[0].perimeter / 300000
                if sub[0].holes_dia:
                    self.man_hour_plate += 1 * sum(sub[0].holes_dia.values())


class ORDER:
    # parts = []

    def __init__(self):
        self.no = ''
        self.name = ''
        self.weight = 0.0
        self.quantity = 0
        self.order_lines = 0
        self.parts = []
        self.nc_path = ''
        self.area = 0.0

    def sum_area(self):
        for single in self.parts:
            self.area += single[0].area * single[1]

    def set_nc_path(self, nc_path):
        self.nc_path = nc_path

    def all_paint_area(self):
        pass

    def manhour_line(self):
        pass

    def manhour_handweld(self):
        pass

    def get_parts(self, part, qty):
        self.parts.append([part, qty])

    def show_parts(self):
        return self.parts

    def sort_by_web(self):
        order_parts_w = reversed(sorted(self.parts, key=lambda parts: (parts[0].web[0].thk, parts[0].web[0].wid,
                                                                       parts[0].web[0].len, parts[0].flange[0].thk,
                                                                       parts[0].flange[0].wid,
                                                                       parts[0].flange[0].len)))
        return order_parts_w

    def sort_by_flange(self):
        order_parts_f = reversed(sorted(self.parts, key=lambda parts: (parts[0].flange[0].thk, parts[0].flange[0].wid,
                                                                       parts[0].flange[0].len, parts[0].web[0].thk,
                                                                       parts[0].web[0].wid, parts[0].web[0].len)))
        return order_parts_f


class BatchPart(PART):
    def __init__(self):
        super().__init__()
        self.order_no = ''
        # pass


class BATCH:
    def __init__(self):
        self.no = 0
        self.orders_quantity = 0
        self.weight = 0.0
        self.quantity = 0
        self.orders = []
        self.batch_parts = []
        self.noneed_parts = []
        self.stacks = []
        self.order_parts_f = []
        self.order_parts_w = []
        self.area = 0.0

    def sum_area(self):
        for single in self.orders:
            self.area += single.area

    def get_orders(self, order):
        self.orders.append(order)

    def get_batch_parts(self):
        for order in self.orders:
            for part in order.parts:
                batch_part = BatchPart()
                batch_part = part[0]  # 构件类
                batch_part.order = order.no

                if batch_part.len >= 1000:
                    self.batch_parts.append([batch_part, part[1], order.no])  # 构件，数量，订单
                else:
                    self.noneed_parts.append([batch_part, part[1], order.no])

    def sort_by_web(self):
        self.order_parts_w = sorted(self.batch_parts, key=lambda parts: (parts[0].web[0].thk, parts[0].web[0].wid,
                                                                         parts[0].web[0].len, parts[0].flange[0].thk,
                                                                         parts[0].flange[0].wid,
                                                                         parts[0].flange[0].len))[::-1]
        return self.order_parts_w

    def sort_by_flange(self):
        self.order_parts_f = sorted(self.batch_parts, key=lambda parts: (parts[0].flange[0].thk, parts[0].flange[0].wid,
                                                                         parts[0].flange[0].len, parts[0].web[0].thk,
                                                                         parts[0].web[0].wid, parts[0].web[0].len))[
                             ::-1]
        return self.order_parts_f

    def batching(self, by_web_or_flange, limit_flange_wt, limit_web_wt):
        # by_web_or_flange , web = 0, flange = 1
        # print('by_web_or_flange', by_web_or_flange)
        if 1 == by_web_or_flange:
            parts = self.order_parts_f
            # print('parts_by_f')
        else:
            parts = self.order_parts_w
            # print('parts_by_w')

        sequence = 0
        stack = 0

        # limit_flange_wt = 4500.0
        # limit_web_wt = 4500.0

        sum_flange_wt = 0.0
        sum_web_wt = 0.0
        temp_qty = 0
        stack_qty = 0
        flange_wid = 0.0
        flange_thk = 0.0
        new_flange_size = ''
        old_flange_size = ''

        # print('limit_web_wt', limit_web_wt)

        for row in parts:
            # 数据准备
            flange_wt = 0
            web_wt = 0
            temp_qty = 0
            sequence += 1


            p_qty = row[1]
            p_no = row[0].no
            p_len = row[0].len
            rs_flange = row[0].flange
            rs_web = row[0].web

            # print('p_qty:', p_qty)

            # 计算flange_wt, web_wt
            flange_wt = row[0].flange_wt
            web_wt = row[0].web_wt

            # print(flange_wt, '----', web_wt)
            # print(p_qty)

            flange_thk = row[0].flange[0].thk
            flange_wid = row[0].flange[0].wid
            web_thk = row[0].web[0].thk
            web_wid = row[0].web[0].wid
            new_flange_size = str(flange_thk)   # + str(flange_wid)  2017/12/20
            if new_flange_size != old_flange_size:
                stack += 1
                sum_flange_wt = 0
                # pass

            # 清理数据
            if (sum_flange_wt + flange_wt) > limit_flange_wt:  # 翼板堆重超
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    sum_flange_wt = 0
                    sum_web_wt = 0
                    stack += 1
                    # sequence += 1
                else:  # 腹板堆重不超
                    sum_flange_wt = 0
                    # sum_web_wt += web_wt  #2017/10/24
                    sum_web_wt = 0   # 2017/12/20
                    stack += 1
                    # sequence += 1
            else:  # 翼板堆重不超    elif sum_flange_wt > limit_flange_wt * 0.5:
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    sum_flange_wt = 0  # 2017/12/20
                    sum_web_wt = 0
                    stack += 1   # 2017/12/20
                    pass
                else:  # 腹板堆重不超
                    # sum_flange_wt = 0
                    # sum_web_wt = 0
                    # stack += 1
                    pass

            # 读一组构件
            # for pcs in range(p_qty):
            # print(p_qty)
            for pcs in range(p_qty):
                if limit_flange_wt >= (sum_flange_wt + flange_wt):  # 翼板堆重不超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        temp_qty += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt += web_wt
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt = web_wt
                        temp_qty = 1
                else:  # 翼板堆重超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        # sum_web_wt += web_wt   # 2017/12/20
                        sub_web_wt = web_wt   # 2017/12/20
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        sum_web_wt = web_wt
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1

            # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
            #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
            #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
            self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
            # print('+++++++++++++++++end of part type ++++++++++++++')
            old_flange_size = new_flange_size
        return self.stacks

    def batching_org_20171020(self, by_web_or_flange, limit_flange_wt, limit_web_wt):
        # by_web_or_flange , web = 0, flange = 1
        # print('by_web_or_flange', by_web_or_flange)
        if 1 == by_web_or_flange:
            parts = self.order_parts_f
            # print('parts_by_f')
        else:
            parts = self.order_parts_w
            # print('parts_by_w')

        sequence = 0
        stack = 0

        # limit_flange_wt = 4500.0
        # limit_web_wt = 4500.0

        sum_flange_wt = 0.0
        sum_web_wt = 0.0
        temp_qty = 0
        stack_qty = 0
        flange_wid = 0.0
        flange_thk = 0.0
        new_flange_size = ''
        old_flange_size = ''

        # print('limit_web_wt', limit_web_wt)

        for row in parts:
            # 数据准备
            flange_wt = 0
            web_wt = 0
            temp_qty = 0
            sequence += 1

            p_qty = row[1]
            p_no = row[0].no
            p_len = row[0].len
            rs_flange = row[0].flange
            rs_web = row[0].web

            # print('p_qty:', p_qty)

            # 计算flange_wt, web_wt
            flange_wt = row[0].flange_wt
            web_wt = row[0].web_wt

            # print(flange_wt, '----', web_wt)
            # print(p_qty)

            flange_thk = row[0].flange[0].thk
            flange_wid = row[0].flange[0].wid
            web_thk = row[0].web[0].thk
            web_wid = row[0].web[0].wid
            new_flange_size = str(flange_thk) + str(flange_wid)

            if new_flange_size != old_flange_size:
                stack += 1
                sum_flange_wt = 0

            # 清理数据
            if (sum_flange_wt + flange_wt) > limit_flange_wt:  # 翼板堆重超
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    sum_flange_wt = 0
                    sum_web_wt = 0
                    stack += 1
                    # sequence += 1
                else:  # 腹板堆重不超
                    sum_flange_wt = 0
                    # sum_web_wt += web_wt   ###2017/10/24
                    stack += 1
                    # sequence += 1
            else:  # 翼板堆重不超    elif sum_flange_wt > limit_flange_wt * 0.5:
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    # sum_flange_wt = 0
                    sum_web_wt = 0
                    # stack += 1
                else:  # 腹板堆重不超
                    # sum_flange_wt = 0
                    # sum_web_wt = 0
                    # stack += 1
                    pass

            # 读一组构件
            # for pcs in range(p_qty):
            # print(p_qty)
            for pcs in range(p_qty):
                if limit_flange_wt >= (sum_flange_wt + flange_wt):  # 翼板堆重不超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        temp_qty += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt += web_wt
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt = web_wt
                        temp_qty = 1
                else:  # 翼板堆重超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        sum_web_wt += web_wt
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        sum_web_wt = web_wt
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1

            # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
            #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
            #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
            self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
            # print('+++++++++++++++++end of part type ++++++++++++++')
            old_flange_size = new_flange_size
        return self.stacks

    def batching_org(self, by_web_or_flange, limit_flange_wt, limit_web_wt):
        # by_web_or_flange , web = 0, flange = 1
        # print('by_web_or_flange', by_web_or_flange)
        if 1 == by_web_or_flange:
            parts = self.order_parts_f
            # print('parts_by_f')
        else:
            parts = self.order_parts_w
            # print('parts_by_w')

        sequence = 0
        stack = 0

        # limit_flange_wt = 4500.0
        # limit_web_wt = 4500.0

        sum_flange_wt = 0.0
        sum_web_wt = 0.0
        temp_qty = 0
        stack_qty = 0
        flange_wid = 0.0
        flange_thk = 0.0
        new_flange_size = ''
        old_flange_size = ''

        # print('limit_web_wt', limit_web_wt)

        for row in parts:
            # 数据准备
            flange_wt = 0
            web_wt = 0
            temp_qty = 0
            sequence += 1

            p_qty = row[1]
            p_no = row[0].no
            p_len = row[0].len
            rs_flange = row[0].flange
            rs_web = row[0].web

            # print('p_qty:', p_qty)

            # 计算flange_wt, web_wt
            flange_wt = row[0].flange_wt
            web_wt = row[0].web_wt

            # print(flange_wt, '----', web_wt)
            # print(p_qty)

            flange_thk = row[0].flange[0].thk
            flange_wid = row[0].flange[0].wid
            web_thk = row[0].web[0].thk
            web_wid = row[0].web[0].wid
            new_flange_size = str(flange_thk) + str(flange_wid)
            if new_flange_size != old_flange_size:
                stack += 1
                sum_flange_wt = 0

            # 清理数据
            if (sum_flange_wt + flange_wt) > limit_flange_wt:  # 翼板堆重超
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    sum_flange_wt = 0
                    sum_web_wt = 0
                    stack += 1
                    # sequence += 1
                else:  # 腹板堆重不超
                    sum_flange_wt = 0
                    sum_web_wt += web_wt
                    stack += 1
                    # sequence += 1
            else:  # 翼板堆重不超    elif sum_flange_wt > limit_flange_wt * 0.5:
                if (sum_web_wt + web_wt) > limit_web_wt:  # 腹板堆重超
                    # sum_flange_wt = 0
                    sum_web_wt = 0
                    # stack += 1
                else:  # 腹板堆重不超
                    # sum_flange_wt = 0
                    # sum_web_wt = 0
                    # stack += 1
                    pass

            # 读一组构件
            # for pcs in range(p_qty):
            # print(p_qty)
            for pcs in range(p_qty):
                if limit_flange_wt >= (sum_flange_wt + flange_wt):  # 翼板堆重不超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        temp_qty += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt += web_wt
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt += flange_wt
                        sum_web_wt = web_wt
                        temp_qty = 1
                else:  # 翼板堆重超
                    if limit_web_wt >= (sum_web_wt + web_wt):  # 腹板堆重不超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        sum_web_wt += web_wt
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1
                    else:  # 腹板堆重超
                        # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
                        #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
                        #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
                        self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
                        stack += 1
                        sequence += 1
                        sum_flange_wt = flange_wt
                        sum_web_wt = web_wt
                        # print('flange ok++++++++web ok++++++++')
                        temp_qty = 1

            # print(stack, ',', sequence, ',', p_no, ',', temp_qty, ',', sum_flange_wt, '---', sum_web_wt, '----',
            #       flange_wid, '*', flange_thk, '---', web_thk, '*', web_wid, '-' * 5,
            #       temp_qty * flange_wt, '-' * 5, temp_qty * web_wt)
            self.stacks.append([stack, sequence, row[0], temp_qty, row[2]])
            # print('+++++++++++++++++end of part type ++++++++++++++')
            old_flange_size = new_flange_size
        return self.stacks


class STACK:
    stacks = []

    def __init__(self):
        self.no = 0
        self.sequance = 0


class SEQUENCE:
    sequence = []

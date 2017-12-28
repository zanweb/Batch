import os
from CamGen import DataTransform


def sub_part_no_get(partno, subpartno):
    if subpartno.split('-')[0] == partno:
        return subpartno
    else:
        return subpartno.split('-')[0]


def revise_mfg_direction():
    pass


def ped_trans_single(stack_no, seq_no, part_qty, in_file_with_path, out_file_with_path):
    data = DataTransform.PedData()
    reader = data.get_data()
    writer = data.set_data()
    data_info = reader.read(in_file_with_path)
    if len(in_file_with_path.split('_')) > 1:
        data_info.header.make_direction = 1
    data_info.header.piece = part_qty
    if data_info:
        writer.write(data_info, out_file_with_path)
        print('No Data to write Peddinghause file!')


def ped_trans(batch, in_fold, out_fold):
    # print('ped-trans----------------------')
    for each in batch:
        subpart_no = sub_part_no_get(each['PartNo'], each['SubPartNo'])

        in_file_with_path = in_fold + '/' + subpart_no + '.nc1'
        in_file_with_path_even = in_fold + '/' + subpart_no + '_even.nc1'
        if os.path.exists(in_file_with_path):
            out_file_with_path = out_fold + '/' + '%d' % each['StackNo'] + '-' + '%d' % each['SeqNo'] + '-' + subpart_no
            ped_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'], in_file_with_path, out_file_with_path)
        elif os.path.exists(in_file_with_path_even):
            out_file_with_path = out_fold + '/' + '%d' % each['StackNo'] + '-' + '%d' % each['SeqNo'] + '-' + subpart_no
            ped_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'], in_file_with_path_even,
                             out_file_with_path)
        else:
            print(subpart_no + ' , this subpart no nc file for Peddinghause!')
            continue


def fmi_flange_trans_single(stack_no, seq_no, part_qty, in_file_with_path):
    data = DataTransform.FMIData()
    reader = data.get_data()
    writer = data.set_data()
    data_info = reader.read(in_file_with_path)
    if len(str(in_file_with_path).split('_')) > 1:  # 这句有问题
        data_info.header.make_direction = 1
    data_info.header.piece = part_qty
    data_info.header.sequence = seq_no
    writer_line = writer.pre_write(data_info)
    return writer_line


def fmi_flange_trans(batch, in_fold, out_fold):
    # 是否要修改为以stack为单位的
    print('fmi-flange-trans----------------------------')
    order_no = batch[0]['OrderNo']
    write_line = []
    out_file_with_path = out_fold + '/' + order_no + '.PCH'
    for each in batch:
        subpart_no = sub_part_no_get(each['PartNo'], each['SubPartNo'])
        in_file_with_path = in_fold + '/' + subpart_no + '.nc1'
        in_file_with_path_even = in_fold + '/' + subpart_no + '_even.nc1'
        if os.path.exists(in_file_with_path):
            this_line = fmi_flange_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'], in_file_with_path)
            write_line.extend(this_line)
        elif os.path.exists(in_file_with_path_even):
            this_line = fmi_flange_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'],
                                                in_file_with_path_even)
            write_line.extend(this_line)
        else:
            print(subpart_no + ' , this subpart no nc file for FMI!')
            continue

    print(write_line)
    data = DataTransform.FMIData()
    writer = data.set_data()
    if write_line:
        writer.save_file(write_line, out_file_with_path)
        print('No Data write to FMI together file!')
    print('run here ---------------')


def fmi_flange_trans_single_file(batch, in_fold, out_fold):
    for each in batch:
        write_line = []
        subpart_no = sub_part_no_get(each['PartNo'], each['SubPartNo'])

        in_file_with_path = in_fold + '/' + subpart_no + '.nc1'
        in_file_with_path_even = in_fold + '/' + subpart_no + '_even.nc1'
        if os.path.exists(in_file_with_path):
            out_file_with_path = out_fold + '/' + '%d' % each['StackNo'] + '-' + '%d' % each[
                'SeqNo'] + '-' + subpart_no + '.PCH'
            write_line = fmi_flange_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'], in_file_with_path)

        elif os.path.exists(in_file_with_path_even):
            out_file_with_path = out_fold + '/' + '%d' % each['StackNo'] + '-' + '%d' % each[
                'SeqNo'] + '-' + subpart_no + '.PCH'
            write_line = fmi_flange_trans_single(each['StackNo'], each['SeqNo'], each['QtyPSeq'],
                                                 in_file_with_path_even)
        data = DataTransform.FMIData()
        writer = data.set_data()
        if write_line:
            writer.save_file(write_line, out_file_with_path)
            print('No Data write to FMI single file!')


if __name__ == '__main__':
    from CamGen import DataTransform

    batch = [{'StackNo': 1, 'SeqNo': 1, 'PartQty': 1, 'PartNo': 'A82'},
             {'StackNo': 1, 'SeqNo': 2, 'PartQty': 6, 'PartNo': 'A293'},
             {'StackNo': 1, 'SeqNo': 3, 'PartQty': 6, 'PartNo': 'A84'},
             {'StackNo': 2, 'SeqNo': 4, 'PartQty': 1, 'PartNo': 'A293'},
             {'StackNo': 2, 'SeqNo': 5, 'PartQty': 1, 'PartNo': 'A84'},
             {'StackNo': 2, 'SeqNo': 6, 'PartQty': 1, 'PartNo': 'A293'},
             {'StackNo': 2, 'SeqNo': 7, 'PartQty': 1, 'PartNo': 'A84'},
             {'StackNo': 3, 'SeqNo': 8, 'PartQty': 6, 'PartNo': 'A308'},
             {'StackNo': 3, 'SeqNo': 9, 'PartQty': 6, 'PartNo': 'A82'},
             {'StackNo': 3, 'SeqNo': 10, 'PartQty': 1, 'PartNo': 'A308'}
             ]
    in_fold = './in_file/1600515801'
    out_fold = './out_file/0_test'
    fmi_flange_trans(batch, in_fold, out_fold)

    # data = DataTransform.FMIData()
    # reader = data.get_data()
    # writer = data.set_data()
    # data_info = reader.read('E:\Zanweb\PythonProgram\Batch\in_file\/1600515801\A82.nc1')
    # print(type(data_info))
    # writer.write(data_info, 'E:\Zanweb\PythonProgram\Batch\Camgen\A82')

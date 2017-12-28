import os


def is_exist_nc(file_with_path):
    # os.path.isfile('test.txt')  # 如果不存在就返回False
    is_exist = os.path.exists(file_with_path)  # 如果目录不存在就返回False
    return is_exist


def has_hole_nc(file_with_path):
    bloc = ['ST',  # Beginning of piece description
            'EN',  # End of piece description
            'BO',  # bloc hole
            'SI',  # bloc numbering
            'AK',  # bloc external contour
            'IK',  # bloc internal contour
            'PU',  # bloc powder
            'K0',  # bloc mark
            'SC',  # bloc cut (Saw, Cutting)
            'TO',  # bloc Tolerance
            'UE',  # bloc Camber
            'PR',  # bloc Profile description
            'KA',  # bloc Bending
            # '**'  # Comment Line
            ]
    dia = []
    # dic_a = {}
    nc_file = open(file_with_path, 'r')
    is_bo = False
    has_hole = False
    for line in nc_file:
        if line.strip() in bloc:
            is_bloc = True
            bloc_name = line.strip()
            if bloc_name == 'BO':
                is_bo = True
                has_hole = True
            else:
                is_bo = False
            if bloc_name == 'EN':
                if has_hole:
                    dic_a = dict((float(a), dia.count(a)) for a in dia)
                    nc_file.close()
                    return dic_a
                else:
                    nc_file.close()
                    return has_hole
        else:
            if is_bo:
                bo = line.split()
                # print(bo)
                dia.append(bo[3])

    # print(dia)
    # dic_a = dict((a, dia.count(a)) for a in dia)
    # print(dic_a)


if __name__ == '__main__':
    file_with_path = "爱仕达11#NC文件\\" + "L125.nc1"
    if is_exist_nc(file_with_path):
        print('OK')
        print(has_hole_nc(file_with_path))
    else:
        print('No')


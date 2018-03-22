import csv


class CsvFile:
    def __init__(self, file_with_path):
        self.file_with_path = file_with_path
        self.seq_info = []

    def get_seq_list(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {}
                    # print(row)
                    info_line['Unit Length'] = row['Unit Length']
                    info_line['Qty'] = row['Qty']
                    info_line['Item'] = str(row['Item']).split('*')[0]  # [:7]
                    info_line['So'] = row['So']
                    info_line['Sorts'] = row['Sorts']

                    # print(info_line['Item'])
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_z_list(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {}
                    info_line['Section'] = row['Section']
                    info_line['Width'] = row['Width']
                    # info_line['Depth'] = row['Depth']
                    # info_line['THK'] = row['THK']
                    # info_line['Flange Width'] = row['Flange Width']
                    # info_line['Leg'] = row['Leg']
                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info

    def get_hole_name(self):
        try:
            with open(self.file_with_path) as f:
                f_csv = csv.DictReader(f)

                for row in f_csv:
                    info_line = {}
                    info_line['HoleType'] = row['HoleType']
                    info_line['HoleName'] = row['HoleName']

                    #
                    self.seq_info.append(info_line)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.seq_info


if __name__ == '__main__':
    csv_f = CsvFile('E:/Zanweb/Bradbury_Import_Test/in_test/Bundle.csv')
    csv_info = csv_f.get_seq_list()
    for row in csv_info:
        print(row)

    csv_z = CsvFile('../Z.csv')
    csv_z_list = csv_z.get_z_list()
    for row in csv_z_list:
        print(row)

from lxml import etree


class Head:
    def __init__(self):
        self.make_direction = 0
        self.order = ''
        self.part_name = ''
        self.length = 0.0
        self.width = 0.0
        self.thickness = 0.0
        self.quantity = 0


class Hole:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0  # not needed

        self.type = ''  # F8D F14D F16O W16D W16O KHSX4


class XmlGen:
    def __init__(self, xml_name):
        self.xml_name = xml_name
        self.header = Head()
        self.holes = []
        self.web_hole_type1 = 'W16D'
        self.web_hole_type2 = 'W16O'

    def creat_element(self, element_name):
        return etree.Element(element_name)

    def creat_sub_element(self, sub_element_name, pre_element=None):
        return etree.SubElement(pre_element, sub_element_name)

    def set_element_attr(self, element, attr_name, attr_value):
        cur_element = element
        cur_element.set(attr_name, attr_value)

    def gen_xml(self, root):
        tree = etree.ElementTree(root)
        tree.write(self.xml_name, pretty_print=True, xml_declaration=True, encoding=u'utf-8')

    def trans_from_nc(self, nc_info):
        self.header.make_direction = nc_info.header.make_direction
        self.header.part_name = nc_info.header.drawing
        self.header.order = nc_info.header.order
        self.header.thickness = float(str(nc_info.header.profile).split('*')[1])
        self.header.width = int(nc_info.header.profile_height)
        self.header.length = int(nc_info.header.length)
        self.header.quantity = int(nc_info.header.quantity)
        # deal with holes
        pre_hole_x = 0.0
        for single_hole in nc_info.holes:
            hole = Hole()
            if single_hole.plane == 'v' and single_hole.reference == 'o' and single_hole.hole_type == '':
                if single_hole.x == pre_hole_x:
                    continue
                hole.x = int(single_hole.x)
                hole.y = 0.0
                hole.type = self.web_hole_type1
                self.holes.append(hole)
                hole = Hole()
                hole.x = int(single_hole.x)
                hole.y = 0.0
                hole.type = self.web_hole_type2
                self.holes.append(hole)
                pre_hole_x = hole.x

    def gen_tree(self):
        orders = self.creat_element('Orders')
        order = self.creat_sub_element('Order', orders)
        self.set_element_attr(order, 'OrderNumber', self.header.order)  # ===============
        job = self.creat_sub_element('Job', order)
        bundle = self.creat_sub_element('Bundle', job)
        part = self.creat_sub_element('Part', bundle)
        self.set_element_attr(part, 'Thickness', str(self.header.thickness))  # ===============
        self.set_element_attr(part, 'Width', str(self.header.width))  # ===============
        self.set_element_attr(part, 'Length', str(self.header.length))  # ===============
        self.set_element_attr(part, 'RequestedQty', str(self.header.quantity))  # ===============
        xml_holes = self.creat_sub_element('Holes', part)
        # print(self.holes)
        for single_hole in self.holes:
            xml_hole = self.creat_sub_element('Hole', xml_holes)
            self.set_element_attr(xml_hole, 'HoleType', single_hole.type)  # ===============
            self.set_element_attr(xml_hole, 'XOffset', str(single_hole.x))  # ===============
            self.set_element_attr(xml_hole, 'YOffset', '0')  # ===============
            self.set_element_attr(xml_hole, 'PartReference', 'Leading')
            self.set_element_attr(xml_hole, 'Station', 'TSC11')

        patterns = self.creat_sub_element('Patterns', part)

        notches = self.creat_sub_element('Notches', part)
        self.gen_xml(orders)


# ===================================================================================


if __name__ == "__main__":
    pass
    # bb_tsc = XmlGen("bbtest.xml")

    # orders = bb_tsc.creat_element('Orders')
    # order = bb_tsc.creat_sub_element('Order', orders)
    # bb_tsc.set_element_attr(order, 'OrderNumber', "1223")  # ===============
    # job = bb_tsc.creat_sub_element('Job', order)
    # bundle = bb_tsc.creat_sub_element('Bundle', job)
    # part = bb_tsc.creat_sub_element('Part', bundle)
    #
    # bb_tsc.set_element_attr(part, 'Thickness', '1.5')  # ===============
    # bb_tsc.set_element_attr(part, 'Width', '369')  # ===============
    # bb_tsc.set_element_attr(part, 'Length', '6895')  # ===============
    # bb_tsc.set_element_attr(part, 'RequestedQty', '1')  # ===============
    # holes = bb_tsc.creat_sub_element('Holes', part)
    #
    # hole = bb_tsc.creat_sub_element('Hole', holes)
    # bb_tsc.set_element_attr(hole, 'HoleType', 'W16O')  # ===============
    # bb_tsc.set_element_attr(hole, 'XOffset', '410')  # ===============
    # bb_tsc.set_element_attr(hole, 'YOffset', '0')  # ===============
    # bb_tsc.set_element_attr(hole, 'PartReference', 'Leading')
    # bb_tsc.set_element_attr(hole, 'Station', 'TSC11')
    #
    # hole = bb_tsc.creat_sub_element('Hole', holes)
    # bb_tsc.set_element_attr(hole, 'HoleType', 'W16D')
    # bb_tsc.set_element_attr(hole, 'XOffset', '35')
    # bb_tsc.set_element_attr(hole, 'YOffset', '0')
    # bb_tsc.set_element_attr(hole, 'PartReference', 'Leading')
    # bb_tsc.set_element_attr(hole, 'Station', 'TSC11')
    #
    # patterns = bb_tsc.creat_sub_element('Patterns', part)
    #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '485')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '410')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '3210')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '3135')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '0')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '0')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '35')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'False')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    # #
    # # pattern01 = bb_tsc.creat_sub_element('Pattern', patterns)
    # # bb_tsc.set_element_attr(pattern01, 'EndOffset', '1535')
    # # bb_tsc.set_element_attr(pattern01, 'RepeatOffset', '75')
    # # bb_tsc.set_element_attr(pattern01, 'LeadOffset', '785')
    # # bb_tsc.set_element_attr(pattern01, 'IsRepeat', 'True')
    # # bb_tsc.set_element_attr(pattern01, 'Reference', 'LeadTrail')
    # # bb_tsc.set_element_attr(pattern01, 'Name', 'W16D+W16O')
    #
    # notches = bb_tsc.creat_sub_element('Notches', part)
    # bb_tsc.gen_xml(orders)

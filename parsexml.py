#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import time
from datetime import datetime


class XMLEx(object):
    def __init__(self):
        pass

    def get_entries(self, xmlfile):
        entry_dict = dict()

        tree = et.parse(xmlfile)
        root = tree.getroot()

        print root.tag, root.attrib, len(root), root.text
        if len(root) > 0:
            for k in range(len(root)):
                print k, root[k].tag, root[k].attrib, len(root[k]), root[k].text
                if len(root[k]) > 0:
                    for i in range(len(root[k])):
                        print "##", k, i, root[k][i].tag, root[k][i].attrib, len(root[k][i]), root[k].text
                        if len(root[k][i]) > 0:
                            for j in range(len(root[k][i])):
                                    print k, i, j, root[k][i][j].tag, root[k][i][j].attrib, len(root[k][i][j]), root[k][i][j].text

        date = datetime.strftime(datetime.now(), '%d.%m.%Y, %H:%M:%S.%f')
        print date
        seconds = float(datetime.strftime(datetime.now(), '%s.%f'))
        print seconds
        print time.time(), "time in seconds"

        #print root[3][30][1].text
        from_date = datetime.strptime(root[3][2][1].text[:19], '%Y-%m-%dT%H:%M:%S')
        to_date= datetime.strptime(root[3][2][2].text[:19], '%Y-%m-%dT%H:%M:%S')
        from_sec = float(datetime.strftime(from_date, '%s.%f'))
        to_sec = float(datetime.strftime(to_date, '%s.%f'))
        print from_sec, from_date, from_sec - seconds
        print to_sec, to_date, to_sec - seconds




if __name__ == "__main__":
    path_to_xmlfile = "nodi.xml"
    test = XMLEx()
    test.get_entries(path_to_xmlfile)



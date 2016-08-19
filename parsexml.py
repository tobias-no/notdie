#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import pprint

class XMLEx(object):
    def __init__(self):
        pass

    def get_entries(self, xmlfile):
        entry_dict = dict()

        tree = et.parse(xmlfile)
        root = tree.getroot()

        #print root.tag, root.attrib, len(root), root.text
        #print root[0].tag, root[0].attrib, len(root[0]), root[0].text
        #print root[1].tag, root[1].attrib, len(root[1]), root[1].text
        #print root[2].tag, root[2].attrib, len(root[2]), root[2].text
        #print root[3].tag, root[3].attrib, len(root[3]), root[3].text


        print root.tag, root.attrib, len(root), root.text
        if len(root) > 0:
            for k in range(len(root)):
                print root[k].tag, root[k].attrib, len(root[k]), root[k].text
                if len(root[k]) > 0:
                    for i in range(len(root[k])):
                        print "##", i, root[k][i].tag, root[k][i].attrib, len(root[k][i]), root[k].text
                        if len(root[k][i]) > 0:
                            for j in range(len(root[k][i])):
                                    print j, root[k][i][j].tag, root[k][i][j].attrib, len(root[k][i][j]), root[k][i][j].text

        print entry_dict 



if __name__ == "__main__":
    path_to_xmlfile = "nodi.xml"
    test = XMLEx()
    test.get_entries(path_to_xmlfile)



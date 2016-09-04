#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import time
import urllib2
from datetime import datetime

#import as global variable 
#protect source path to be pushed on github
#disclaimer for data source can be found there
from source_path import source_path 


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
        print "blub", from_sec, from_date, from_sec - seconds
        print "lbub", to_sec, to_date, to_sec - seconds

    def entry_iter(self, xmlfile):
        self.entry_dict = dict()
        tree = et.parse(xmlfile)
        root = tree.getroot()
        for entry in root.iter("entry"):
            self.entry_dict[(entry[1].text[:19], entry[0].text)] = {}
            for i in range(1, len(entry)):
                self.entry_dict[(entry[1].text[:19], entry[0].text)][entry[i].tag] = entry[i].text

            from_sec = self.convert_to_sec(self.entry_dict[(entry[1].text[:19], entry[0].text)]['from'][:19], '%Y-%m-%dT%H:%M:%S')
            to_sec = self.convert_to_sec(self.entry_dict[(entry[1].text[:19], entry[0].text)]['to'][:19], '%Y-%m-%dT%H:%M:%S')

            self.entry_dict[(entry[1].text[:19], entry[0].text)]['from_sec'] = from_sec
            self.entry_dict[(entry[1].text[:19], entry[0].text)]['to_sec'] = to_sec

        self.update_diffsec()


    def update_diffsec(self):
        now_sec = float(datetime.strftime(datetime.now(), '%s.%f'))
        for k, v in self.entry_dict.items():
            v['diff_from'] = now_sec - v['from_sec']
            v['diff_to'] = now_sec - v['to_sec']

    
    def convert_to_sec(self, input_time, src_format):
        return float(datetime.strftime(datetime.strptime(input_time, src_format), '%s.%f'))


    def filter_dict(self):
        now_sec = float(datetime.strftime(datetime.now(), '%s.%f'))
        apo_list = []
        for k, v in self.entry_dict.items():
            print v['name'], v['from'][:19], v['to'][:19]
            from_sec = self.convert_to_sec(v['from'][:19], '%Y-%m-%dT%H:%M:%S')
            to_sec = self.convert_to_sec(v['to'][:19], '%Y-%m-%dT%H:%M:%S')
            #print v['name'], from_sec, to_sec, now_sec - from_sec, now_sec - to_sec
            apo_list.append([now_sec - from_sec, now_sec - to_sec, v['name']])
        print v.keys()
        print sorted(apo_list)


    def get_online_data(self):
        xml_file = "nodie.xml"
        for zz in range(10):
            try:#
                stream = urllib2.urlopen(source_path)
                if stream.msg == 'OK':
                    with open(xml_file, "w") as f:
                        f.write(stream.read())
                    stream.close()
                    return True
            except BaseException as e:
                print zz, "xml retrieval from online source failed:", e, "...retry"
                time.sleep(2)
                if zz == 9:
                    return False


if __name__ == "__main__":
    path_to_xmlfile = "nodie.xml"
    test = XMLEx()
    #print test.get_online_data()
    test.entry_iter(path_to_xmlfile)
    print test.entry_dict
    #test.filter_dict()
    #test.get_entries(path_to_xmlfile)



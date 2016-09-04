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



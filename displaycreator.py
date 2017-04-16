#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
import urllib2
import json

from parsexml import XMLEx
from datetime import date
from source_path import tft_init_func, putiton

path_to_xmlfile = "nodie.xml"

class DisplayCreator(object):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((320,240))
        try:
            self.init_tft()
        except:
            print("TFT initialization failed: not running on RPi?")

    def init_tft(self):
        tft_init_func()

    def create_bmp(self, entry_dict, entry_key, nowbmp):
        font_standard = pygame.font.SysFont("freesans", 15)
        font_date = pygame.font.SysFont("freesans", 13)
        font_apo = pygame.font.SysFont("freesans", 18, True)
        font_tiny = pygame.font.SysFont("freesans", 8)
        if nowbmp:
            first_line = u"Jetzt Notdienst:"
        else:
            first_line = u"Nächster Notdienst:"
        label_first = font_standard.render(first_line, 1, (255,255,255))
        label_date = font_date.render(u"von {}  8.30 Uhr   bis {}  8.30 Uhr".format(entry_dict[entry_key]['from_date'], 
                                                                               entry_dict[entry_key]['to_date']), 
                                                                               1, (255,255,255))
        label_apo = font_apo.render(u"{}".format(entry_dict[entry_key]['name']), 1, (255,0,0))
        label_street = font_standard.render(u"{}".format(entry_dict[entry_key]['street']), 1, (255,255,255))
        label_loc = font_standard.render(u"{} {}".format(entry_dict[entry_key]['zipCode'], entry_dict[entry_key]['location']), 1, (255,255,255))
        label_phone = font_standard.render(u"Tel  {}".format(entry_dict[entry_key]['phone']), 1, (255,255,255))
        label_discl = font_tiny.render(u"Notdienstdaten durch die Landesapothekerkammer Baden-Württemberg zur Verfügung gestellt", 1, (255,255,255))

        self.window.fill(pygame.Color(0,0,0))

        self.window.blit(label_first, (0,0))
        self.window.blit(label_date, (0,30))
        self.window.blit(label_apo, (0,70))
        self.window.blit(label_street, (0,130))
        self.window.blit(label_loc, (0,150))
        self.window.blit(label_phone, (0,170))
        self.window.blit(label_discl, (0,230))

        try:
            pygame.image.save(self.window, "/ram/tmp.bmp")
            putiton("ram/tmp.bmp")
            time.sleep(4)
        except BaseException as e:
            print("{}: Not running on RPi? -> saving bmp in current folder".format(e))
            pygame.image.save(self.window, "tmp.bmp")
            time.sleep(4)


    def hamster_wheel(self, update=True):
        xe = XMLEx(path_to_xmlfile)
        if update:
            print(xe.get_online_data())
        for k in xe.get_phs(offset_h=0):
            self.create_bmp(xe.entry_dict, k, True) 

        for k in xe.get_phs(offset_h=24):
            self.create_bmp(xe.entry_dict, k, False) 

        if xe.get_xmlstatus() > 0:
            self.update_needed=True
        else:
            self.update_needed=False


if __name__ == "__main__":
    with open("notdie_pid.txt", 'w') as pidfile:
        pidfile.write(str(os.getpid()))
    dc = DisplayCreator()
    dc.hamster_wheel(True) #first run should always update
    i=0
    while True:
        i+=1; print(i)
        if i%10 == 0 and dc.update_needed==True:
            dc.hamster_wheel(update=True)
        else:
            dc.hamster_wheel(update=False)





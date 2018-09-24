#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
import urllib2
import json

from datetime import date



url_feiertage_bw = "http://feiertage.jarmedia.de/api/?jahr={}&nur_land=BW".format(date.today().year)

feiertage_file = "feiertage_{}.json".format(date.today().year)

if not os.path.exists(feiertage_file):
    print url_feiertage_bw
    for zz in range(10):
        try:
            stream = urllib2.urlopen(url_feiertage_bw)
            if stream.msg == 'OK':
                with open(feiertage_file, "w") as f:
                    f.write(stream.read())
                stream.close()
        except BaseException as e:
            print zz, "xml retrieval from online source failed:", e, "...retry"
            time.sleep(2)
            if zz == 9:
                pass

with open(feiertage_file) as f:
    feiertage = json.load(f)

for k, v in feiertage.items():
    print v['datum'], k

exit()

pygame.init()
window = pygame.display.set_mode((320,240))



#os.system("tft_init")
#os.system("tft_clear")
#os.system("tft_pwm 80")

font0 = pygame.font.SysFont("freesans", 30)
loc = "Künzelsau"
label0 = font0.render(loc.decode('utf-8'), 1, (255,255,255))

window.fill(pygame.Color(0,0,0))

window.blit(label0, (0,100))

pygame.image.save(window, "temp.bmp")
#pygame.image.save(window, "/ram/temp.bmp")



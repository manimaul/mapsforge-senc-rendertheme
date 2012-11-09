#!/usr/bin/env python
#-*- coding: utf-8 -*-
# by Will Kamp <manimaul!gmail.com>
# use this anyway you want

from xml.dom.minidom import parseString
import os

f = open("chartsymbols.xml", "r")
lines = f.read()
f.close()

dom = parseString(lines)
for symEle in dom.getElementsByTagName("symbol"):
    name = symEle.getElementsByTagName("name")[0].firstChild.nodeValue
    btmEle = symEle.getElementsByTagName("bitmap")
    if len(btmEle) > 0:
        locEle = btmEle[0].getElementsByTagName("graphics-location")
        width = int( btmEle[0].attributes["width"].value )
        height = int( btmEle[0].attributes["height"].value )
        x = locEle[0].attributes["x"].value
        y = locEle[0].attributes["y"].value
        print "creating: %s" %(name)
        #imagemagick to the rescue
        cmd = "convert rastersymbols-day.png -crop %sx%s+%s+%s ../rendertheme/symbols/%s.png" %(width, height, x, y, name)
        os.popen(cmd)
        cmd = "convert rastersymbols-dusk.png -crop %sx%s+%s+%s ../rendertheme/symbols/dusk/%s.png" %(width, height, x, y, name)
        os.popen(cmd)
        cmd = "convert rastersymbols-dark.png -crop %sx%s+%s+%s ../rendertheme/symbols/dark/%s.png" %(width, height, x, y, name)
        os.popen(cmd)
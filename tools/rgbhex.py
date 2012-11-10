#!/usr/bin/env python
#-*- coding: utf-8 -*-
# by Will Kamp <manimaul!gmail.com>
# use this anyway you want

def rgbtohex(r, g, b):
    return _rgbtohex((r,g,b))

def _rgbtohex(rgbTuple):
    r, g, b = rgbTuple
    return hex(r) + hex(g)[2:] + hex(b)[2:]

def hextorgb(hexString):
    h1, h2, h3 = hexString[0:4], '0x' + hexString[4:6], '0x' + hexString[6:8]
    r, g , b = int(h1, 16), int(h2, 16), int(h3, 16)
    return (r, g, b)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

#manimaul@gmail.com
#bounding box calculator for mapsforge

from osgeo import ogr
import sys, os.path

def getBbox(mPath):
    ds = ogr.Open(mPath)
    if ds is None:
        print "file:", mPath, "is not an ogr readable file!"
        return (None, None, None, None)

    layer_list = []    
    maxLatitude = -90.0
    maxLongitude = -180.0
    minLatitude = 90.0
    minLongitude = 180.0

    #get a list of layers
    for lnum in range(ds.GetLayerCount()):
        layer = ds.GetLayer(lnum)
        if layer_list.count(layer.GetName()) == 0:
            layer_list.append(layer.GetName())
    
    for lyr_name in layer_list:
        #print "Reading layer: ", lyr_name
        lyr = ds.GetLayerByName(lyr_name)
        lyr.ResetReading()
        
        for feat in lyr:
            # get bounding coords in minx, maxx, miny, maxy format
            gr = feat.GetGeometryRef()
            if gr is not None:
                env = gr.GetEnvelope()
                minLongitude = min(minLongitude, env[0])
                maxLongitude = max(maxLongitude, env[1])
                minLatitude = min(minLatitude, env[2])
                maxLatitude = max(maxLatitude, env[3])
                #print [env[0], env[1], env[2], env[3]]
    return (minLatitude, minLongitude, maxLatitude, maxLongitude)

if __name__ == "__main__":
    if len(sys.argv) is 1:
        print "please supply a path to an ogr readable file path as an argument!"
    elif os.path.isfile(sys.argv[-1]):
        print "opening: ", sys.argv[-1]
        print "bounding box found as: minLat, minLon, maxLat, maxLon"
        print "%s,%s,%s,%s"%(getBbox(sys.argv[-1]))
    else:
        print sys.argv[-1], "is not a valid file path"

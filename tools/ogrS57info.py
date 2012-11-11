#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Will Kamp <manimaul!gmail.com>
# This will find the appropriate zxy tiled map optimal zoom level for a S57 chart
# Bounding box center point and scale also available
# Accounts for latitude distortion of scales

import math
from shapely.geometry import Point
from pyproj import Proj
from osgeo import ogr

class s57():
    def __init__(self, s57_path):
        
        self.s57_path = s57_path
        self.s57_ds = ogr.Open(s57_path, 0) #0 means read only
        if self.s57_ds == None:
            print "open S57 failed:", self.s57_path
        
        elif not self.s57_ds.GetDriver().GetName() == "S57":
            print "not and S57 file:", self.s57_path
        
        self.scale = None
        self.box = None
        self.center = None
        self.layerList = []
        
        if self.s57_ds != None:    
            layer = self.s57_ds.GetLayerByName("DSID") #BEACON SPECIAL PURPOSE
            fieldList = self._getLayerFields(layer)
            self.fieldValues = self._getLayerFieldValues(layer.GetNextFeature(), fieldList)
            
            for layer in self.s57_ds:
                self.layerList.append(layer.GetName())
        else:
            self.fieldValues = {}
    
    def getLayerGeometryType(self, layerName):
        if self.layerList.count(layerName) > 0:
            layer = self.s57_ds.GetLayerByName(layerName)
            layer.ResetReading()
            feature = layer.GetNextFeature()
            geometryType = 0;
            if feature is not None:
                geomRef = feature.GetGeometryRef()
                if geomRef is not None:
                    geometryType = geomRef.GetGeometryType()
        
            if (geometryType == ogr.wkbPoint or
                geometryType == ogr.wkbPoint25D):
                return "POINT"
            elif (geometryType == ogr.wkbLineString or
                  geometryType == ogr.wkbLinearRing or
                  geometryType == ogr.wkbLineString25D):
        #         geometryType == ogr.wkbLinearRing25D does not exist
                return "LINESTRING"
            elif (geometryType == ogr.wkbPolygon or
                  geometryType == ogr.wkbPolygon25D):
                return "POLYGON"
            elif (geometryType == ogr.wkbMultiPoint or
                  geometryType == ogr.wkbMultiLineString or
                  geometryType == ogr.wkbMultiPolygon or
                  geometryType == ogr.wkbGeometryCollection or
                  geometryType == ogr.wkbMultiPoint25D or
                  geometryType == ogr.wkbMultiLineString25D or
                  geometryType == ogr.wkbMultiPolygon25D or
                  geometryType == ogr.wkbGeometryCollection25D):
                return "COLLECTION"
    
    def getLayerFields(self, layerName):
        if self.layerList.count(layerName) > 0:
            layer = self.s57_ds.GetLayerByName(layerName)
            return self._getLayerFields(layer)
        
    def getLayerList(self):
        return self.layerList
        
    def getCenterPoint(self):
        if self.center is None:
            if self.getBoundingBox() is not None:
                maxLat = self.box[2]
                minLat = self.box[0]
                centerLat = minLat + (maxLat - minLat) / 2
                minLon = self.box[1]
                maxLon = self.box[3]
                centerLon = minLon + (maxLon - minLon) / 2
                self.center = (centerLat, centerLon)
        return self.center
            
    
    def getBoundingBox(self):
        #minLat, minLon, maxLat, maxLon
        if self.box is None and self.s57_ds != None:
            layer_list = []    
            maxLatitude = -90.0
            maxLongitude = -180.0
            minLatitude = 90.0
            minLongitude = 180.0
        
            #get a list of layers
            for lnum in range(self.s57_ds.GetLayerCount()):
                layer = self.s57_ds.GetLayer(lnum)
                if layer_list.count(layer.GetName()) == 0:
                    layer_list.append(layer.GetName())
            
            for lyr_name in layer_list:
                #print "Reading layer: ", lyr_name
                lyr = self.s57_ds.GetLayerByName(lyr_name)
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
            self.box = (minLatitude, minLongitude, maxLatitude, maxLongitude)
        return self.box
    
    def getScale(self):
        if self.scale is None:
            if self.fieldValues.has_key("DSPM_CSCL"):
                self.scale = int(self.fieldValues["DSPM_CSCL"])
        return self.scale
    
    def getZoom(self):
        if self.getScale() > -1 and self.getCenterPoint() is not None:
            tweakPercent = .70
            latitude = self.center[0]
            truescale = self.scale * self._latitudedistortion(latitude) * tweakPercent
            z = 30;
            while truescale > 1:
                truescale = truescale / 2;
                z -= 1;
            return z
                
    def _getLayerFields(self, layer):
        featureDefinition = layer.GetLayerDefn()
        fieldNames = []
        fieldCount = featureDefinition.GetFieldCount()
        for j in range(fieldCount):
            fieldNames.append(featureDefinition.GetFieldDefn(j).GetNameRef())
        return fieldNames

    def _getLayerFieldValues(self, ogrfeature, fieldList):
        fieldValues = {}
        for i in range(len(fieldList)):
            fieldValues[fieldList[i]] = ogrfeature.GetFieldAsString(i)
        return fieldValues

    def _haversinedistance(self, origin, destination):
        lon1, lat1 = origin
        lon2, lat2 = destination
        radius = 6371 #kilometers
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d * 1000 #meters
    
    def _cartesiandistance(self, origin, destination):
        lon1, lat1 = origin
        lon2, lat2 = destination
        proj = Proj(init="epsg:3785") # spherical mercator, should work anywhere
        point1 = proj(lon1, lat1)
        point2 = proj(lon2, lat2)
        point1_cart = Point(point1)
        point2_cart = Point(point2)
        return point1_cart.distance(point2_cart) #meters
    
    def _latitudedistortion(self, latitude):
        origin = (0, latitude)
        destination = (1, latitude)
        hdist = self._haversinedistance(origin, destination)
        cdist = self._cartesiandistance(origin, destination)
        return cdist/hdist

if __name__== "__main__":
    #mpath = "/home/will/zxyCharts/ENC_ROOT/REGION_15/ENC_ROOT/CATALOG.031"
    mpath = "/home/will/zxyCharts/ENC_ROOT/REGION_15/ENC_ROOT/US1WC01M/US1WC01M.000"
    myS57 = s57(mpath)
    print myS57.getScale()
    print myS57.getBoundingBox()
    print myS57.getCenterPoint()
    print myS57.getZoom()
    print myS57.getLayerList()
    print myS57.getLayerFields("LIGHTS")
    print myS57.getLayerGeometryType("LIGHTS")

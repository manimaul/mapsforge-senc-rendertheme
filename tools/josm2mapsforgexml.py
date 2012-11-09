#!/usr/bin/env python
#-*- coding: utf-8 -*-
# by Will Kamp <manimaul!gmail.com>
# use this anyway you want

from sys import getsizeof, exit, argv
import os

version=" version=\'1\'"
timestamp=" timestamp=\'2012-01-01T00:00:00.0+11:00\'"
changeset=" changeset=\'0\'"
newfileName = "josm2mapsforge.xml"

class JosmFile():
    def __init__(self, filePath):
        self.josmfile = open(filePath, "r")
        self.bytes = os.stat(filePath).st_size
        self.xmlLine = ""
        self.char = ""

        self.replacements = ""
        self.count = 0
        self.debug = False
        #self.newfile = open()
        
        fileDir = os.path.split(os.path.abspath(filePath))[0]
        tmp = fileDir+"/tmp.xml"
        outPath = fileDir+"/"+newfileName
        self.newJosmFile = open(tmp, "w")
        self._addMissingData()
        self.newJosmFile.close()
        self.josmfile.close()
        
        command = "cat %s | tidy -utf8 -xml -w 255 -i -c -q -asxml > %s && rm %s" %(tmp, outPath, tmp)
        os.popen(command);
        
        
        
        
        
    def _addMissingData(self):
        for _byte in range(self.bytes):
            self.char = self.josmfile.read(1)
            self.xmlLine += self.char
            
            #this probably is not an xml file if a line grows to 512KB
            if getsizeof(self.xmlLine) > 524288:
                exit(1)
            elif (self.char == ">"):
                self.xmlLine = self.xmlLine.strip()
                if self.xmlLine.startswith("<node"):
                    if self.xmlLine.find("version") < 0:
                        self.replacements += version
                    if self.xmlLine.find("changeset") < 0:
                        self.replacements += changeset
                    if self.xmlLine.find("timestamp") < 0:
                        self.replacements += timestamp
                    if self.replacements != "":
                        if self.xmlLine.endswith("/>"):
                            endCap = "/>"
                        else:
                            endCap = ">"
                        self.count +=1
                        if self.debug:
                            print self.xmlLine
                        self.xmlLine = self.xmlLine.replace(endCap, self.replacements+endCap)
                        if self.debug:
                            print self.xmlLine
                elif self.xmlLine.startswith("<way"):
                    if self.xmlLine.find("version") < 0:
                        self.replacements += version
                    if self.xmlLine.find("changeset") < 0:
                        self.replacements += changeset
                    if self.xmlLine.find("timestamp") < 0:
                        self.replacements += timestamp
                    if self.replacements != "":
                        if self.xmlLine.endswith("/>"):
                            endCap = "/>"
                        else:
                            endCap = ">"
                        self.count += 1
                        if self.debug:
                            print self.xmlLine
                        self.xmlLine = self.xmlLine.replace(endCap, self.replacements+endCap)
                        if self.debug:
                            print self.xmlLine
                self.newJosmFile.write(self.xmlLine);
                self.xmlLine = ""
                self.replacements = ""   
        print "Added missing fields to %s ways and nodes" %(self.count)
        
if __name__=="__main__":
    print "WARNING! use this utility ONLY if you know what you are doing and what this does!\n"
    print "The purpose of this utility is to make files saved by JOSM readable by osmosis for the sole purpose of importing into mapsforge.\n"
    print version.lstrip() + changeset + timestamp + " will be added if they do not exist in every node and way.\n"
    if len(argv) is 1:
        print "Please supply a path to an osm/xml targetfile... targetfile will NOT be overwritten"
        print "%s will be created in the same directory as targetfile" %(newfileName)
    elif os.path.isfile(argv[-1]):
        JosmFile(argv[-1])
    else:
        print "%s is not a valid path!" %(argv[-1])
        #JosmFile("/home/will/zxyCharts/ENC_ROOT/coastlines/focus/out-sorted-split.osm")
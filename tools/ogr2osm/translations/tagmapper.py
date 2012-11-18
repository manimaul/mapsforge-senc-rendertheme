#!/usr/bin/env python
#-*- coding: utf-8 -*-
# by Will Kamp <manimaul!gmail.com>
# use this anyway you want

from xml.dom.minidom import parseString

DEBUG = False

def getUnMatched(layername, tags):
    newTags = {}
    
    if DEBUG:
        print tags
        
    if layername == "LIGHTS":
        #use default light
        newTags = {'LIGHTS': 'LIGHTDEF'}
    return newTags

class TagMapper():
    def __init__(self, xmlPath):
        f = open(xmlPath, "r")
        lines = f.read()
        dom = parseString(lines)
        f.close()
        self.lookups = dom.getElementsByTagName("lookup")
        
    def LookupTag(self, layer, tags):
        newtags = {}
        matches = {} #nummatches: instructions
        numatches = 0
        for lookup in self.lookups:
            name = lookup.attributes["name"].value
            if name == layer:
                table = lookup.getElementsByTagName("table-name")[0].firstChild.nodeValue
                
                if table == "Paper":
                    attributes = lookup.getElementsByTagName("attrib-code")
                    instruction = None
                    for attrEle in attributes:
                        attrib = attrEle.firstChild.nodeValue #ex COLOUR4,3,4  or CATSPM44 or BCNSHP1
                        key = attrib[0:6] #first six of the attrib needs to math a key
                        if tags.has_key(key):
                            if tags.get(key) == attrib[6:len(attrib)]:
                                numatches += 1
                                if DEBUG:
                                    print "found number:", numatches
                                instruction = lookup.getElementsByTagName("instruction")[0].firstChild.nodeValue
                                matches[numatches] = instruction
        
        if numatches == 0:
            for lookup in self.lookups:
                name = lookup.attributes["name"].value
                if name == layer:
                    table = lookup.getElementsByTagName("table-name")[0].firstChild.nodeValue
                    if table == "Plain":
                        instruction = lookup.getElementsByTagName("instruction")[0].firstChild.nodeValue
                        matches[numatches] = instruction
        
        if len(matches) > 0:
            index = max(matches.keys())
            if DEBUG:
                print "tagmapper found best match"
            instruction = matches[index]
            newtags[layer] = instruction.split(";")[0][3:-1].rstrip(",ORIENT")
        
        if len(newtags) == 0:
            if DEBUG:
                print "tagmapper did not find a match... checking for a default"
            newtags = getUnMatched(layer, tags)
                
        return newtags
    
if __name__ == "__main__":
    tm = TagMapper("/home/will/Documents/workspace-python/mapsforge-senc-rendertheme/opencpn.org-S57-reference/chartsymbols.xml")
    layer = 'BOYSPP'
    sampletags = {'TXTDSC': '', 'RCID': '11', 'PRIM': '1', 'NINFOM': '', 'DATEND': '', 'SORIND': 'US,US,reprt,11thCGD,LNM 35/10', 'COLPAT': '', 'AGEN': '550', 'GRUP': '2', 'MARSYS': '', 'DATSTA': '', 'FFPT_RIND': '(1:2)', 'PERSTA': '', 'SORDAT': '20100831', 'PICREP': '', 'COLOUR': '6', 'SCAMAX': '', 'NOBJNM': '', 'INFORM': '', 'LNAM': '022606EC59321059', 'SCAMIN': '8000000', 'VERACC': '', 'PEREND': '', 'STATUS': '8', 'LNAM_REFS': '(1:022606EC57C91059)', 'NTXTDS': '', 'CATSPM': '9', 'RVER': '1', 'RECDAT': '', 'OBJL': '19', 'VERLEN': '', 'OBJNAM': '46006', 'FIDS': '4185', 'RECIND': '', 'BOYSHP': '7', 'FIDN': '116152626', 'NATCON': '', 'CONRAD': ''}
    print tm.LookupTag(layer, sampletags);
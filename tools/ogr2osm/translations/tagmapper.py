#!/usr/bin/env python
#-*- coding: utf-8 -*-
# by Will Kamp <manimaul!gmail.com>
# use this anyway you want

from xml.dom.minidom import parseString

class TagMapper():
    def __init__(self):
        f = open("/home/will/Documents/workspace-python/mapsforge-senc-rendertheme/opencpn.org-S57-reference/chartsymbols.xml", "r")
        lines = f.read()
        dom = parseString(lines)
        f.close()
        self.lookups = dom.getElementsByTagName("lookup")
        
    def LookupTag(self, layer, tags):
        newtags = {}
        for lookup in self.lookups:
            #name = lookEle.getElementsByTagName("name")[0].firstChild.nodeValue
            name = lookup.attributes["name"].value
            if name == layer:
                table = lookup.getElementsByTagName("table-name")
                if table[0].firstChild.nodeValue == "Paper":
                    attributes = lookup.getElementsByTagName("attrib-code")
                    matches = []
                    instruction = None
                    for attrEle in attributes:
                        attrib = attrEle.firstChild.nodeValue #COLOUR4,3,4  or CATSPM44 or BCNSHP1
                        key = attrib[0:6] #first six of the attrib needs to math a key
                        if tags.has_key(key):
                            if tags.get(key) == attrib[6:len(attrib)]:
                                matches.append(attrib)
                                instruction = lookup.getElementsByTagName("instruction")[0].firstChild.nodeValue
                        else:
                            break
                    if len(matches) == len(attributes) != 0:
                        print "tagmapper found match"
                        #print matches
                        tag = "SENC" + instruction.split(";")[0][0:2]
                        newtags[tag] = instruction.split(";")[0][3:-1]
                        
        return newtags
    
if __name__ == "__main__":
    tm = TagMapper()
    layer = 'BCNSPP'
    tags = {'TXTDSC': '', 'RCID': '1', 'PRIM': '1', 'NINFOM': '', 'DATEND': '', \
           'SORIND': 'US,US,reprt,17thCGD,LNM 24/04', 'COLPAT': '', 'AGEN': '550', \
           'GRUP': '2', 'MARSYS': '', 'ELEVAT': '', 'DATSTA': '', 'FFPT_RIND': '(2:2,2)', \
           'PERSTA': '', 'SORDAT': '20040615', 'PICREP': '', 'COLOUR': '', 'VERDAT': '', \
           'SCAMAX': '', 'NOBJNM': '', 'INFORM': '', 'LNAM': '022606EC592D1059', \
           'VERACC': '', 'PEREND': '', 'BCNSHP': '4', 'STATUS': '1', 'HEIGHT': '', \
           'LNAM_REFS': '(2:022606EC57EA1059,022606EC4D831059)', 'NTXTDS': '', \
           'CATSPM': '27', 'NATCON': '', 'RECDAT': '', 'OBJL': '9', 'VERLEN': '', \
           'OBJNAM': 'Lowrie Island Light', 'CONDTN': '', 'FIDS': '4185', 'RECIND': '', \
           'SCAMIN': '8000000', 'FIDN': '116152621', 'CONVIS': '', 'RVER': '1', 'CONRAD': ''}
    print tm.LookupTag(layer, tags);
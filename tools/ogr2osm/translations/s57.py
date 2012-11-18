import tagmapper

tm = tagmapper.TagMapper("/home/will/Documents/workspace-python/mapsforge-senc-rendertheme/opencpn.org-S57-reference/chartsymbols.xml")

####parameters
theseLayers = ['LIGHTS', 'BOYSPP', 'LNDARE', 'BCNLAT', 'BCNSPP', 'BUAARE', 'BOYSAW', 'BOYSPP', 'WRECKS']
layername = None

def filterLayer(layer):
    if layer is None:
        return None
    
    if theseLayers.count(layer.GetName()) > 0:
        global layername
        layername = layer.GetName()
        return layer
    else:
        return None

def filterTags(tags):
    if tags is None:
        return tags
    
    scamin = tags["SCAMIN"]
    #print "filtering tags for layer:" + layername + scamin
    
    
    #lookup new tags
    newTags = tm.LookupTag(layername, tags)
    
    #reattach scamin tag
    newTags["SCAMIN"] = scamin
    
    return newTags
        

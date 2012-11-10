import tagmapper

tm = tagmapper.TagMapper()

####parameters
skiplayers = ["M_QUAL", "M_NSYS", "M_NPUB", "M_COVR", "DSID", "C_ASSO", "SOUNDG"]
layername = ""

def filterLayer(layer):
    if layer is None:
        return layer
    
    if skiplayers.count(layer.GetName()) > 0:
        return None
    
    else:
        layername = layer.GetName()
        return layer

def filterTags(tags):
    print "filtering tags for layer:" + layername
    if tags is None:
        return tags
    return tm.LookupTag(layername, tags)

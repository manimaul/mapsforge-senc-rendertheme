####parameters
#onlytheselayers = ["ne_110m_ocean"]
keyvaluereplacements = {"FeatureCla":("natural","coastline")}
usethesekeys = []

uvmfeatures = []

def filterTags(tags):
    if tags is None:
        return
    
    newtags = {}
    for (key, value) in tags.items():
        if keyvaluereplacements.has_key(key):
            newkey = keyvaluereplacements[key][0]
            newvalue = keyvaluereplacements[key][1]
            newtags[newkey] = newvalue
        elif usethesekeys.count(key) > 0:
            newtags[key] = value
    return newtags

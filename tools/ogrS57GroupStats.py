from FilePathSearch import FilePathSearch
import ogrS57info

class s57Stats():
    def __init__(self, directory):
        fps = FilePathSearch(directory)
        
        self.scalemap = {} #scale: path
        self.scales = [] #list of unique scales
        self.layermap = {} #path: layers
        self.layers = [] #list of unique layers
        self.zoommap = {} #zoom: path
        self.zooms = [] #list of unique zooms
        skiplayers = ["M_QUAL", "M_NSYS", "M_NPUB", "M_COVR", "DSID", "C_ASSO"]
        
        self.geommap = {} #layer: geomtype
        
        for s57path in fps.getfilePaths():
            s57 = ogrS57info.s57(s57path)
            
            scale = s57.getScale()
            self.scalemap[scale] = self.scalemap.get(scale, [])
            self.scalemap[scale].append(s57path)
            
            zoom = s57.getZoom()
            self.zoommap[zoom] = self.zoommap.get(zoom, [])
            self.zoommap[zoom].append(s57path)
            
            layers = s57.getLayerList()
            for lyr in layers:
                if skiplayers.count(lyr) > 0:
                    layers.remove(lyr)
            self.layermap[s57path] = layers
            
            for lyr in s57.getLayerList():
                if self.layers.count(lyr) == 0 and skiplayers.count(lyr) == 0:
                    self.layers.append(lyr)
                    self.geommap[lyr] = s57.getLayerGeometryType(lyr)
 
        for key in self.scalemap.keys():
            self.scales.append(key)
            
        for key in self.zoommap.keys():
            self.zooms.append(key)
        
        self.layers.sort()
        self.scales.sort()
        self.zooms.sort()
    
    def getLayerGeometryType(self, layer):
        if self.geommap.has_key(layer) > 0:
            return self.geommap[layer]
    
    def getRenderableLayersAtPath(self, sPath):
        if self.layermap.has_key(sPath):
            return self.layermap[sPath]
    
    def getListOfZooms(self):
        return self.zooms
    
    def getFilesAtZoom(self, zoom):
        if self.zoommap.has_key(zoom):
            return self.zoommap[zoom]
    
    def getListOfScales(self):
        return self.scales
    
    def getFilesAtScale(self, scale):
        if self.scalemap.has_key(scale) > 0:
            return self.scalemap[scale]
        
    def getListOfLayers(self):
        return self.layers

#NOT USED
#0,1
#--
#SET0
#2,3,4
#
#SET1
#5,6,7
#
#SET2
#8,9,10
#
#SET3
#11,12,13
#
#SET4
#14,15,16,17
#--
#NOT USED
#18+
def getSet(zoom):
    sets = {"z2-4": [2,3,4], "z5-7": [5,6,7], "z8-10": [8,9,10], "z11-13": [11,12,13], "z14-17": [14,15,16,17]}
    for key in sets:
        if sets[key].count(zoom) == 1:
            return key

if __name__ == "__main__":
    
    encroot = "/home/will/zxyCharts/ENC_ROOT/REGION_15/ENC_ROOT"
    stats = s57Stats(encroot)
    print stats.getListOfLayers()
    print stats.getListOfZooms()
    print stats.getListOfScales()
    #print stats.getLayerGeometryType("BOYCAR")
    #print stats.getFilesAtZoom(7)
    #print stats.getFilesAtScale(80000)
    
    
    
    
 

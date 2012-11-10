from FilePathSearch import FilePathSearch
import ogrS57info

class s57Stats():
    def __init__(self, directory):
        fps = FilePathSearch(directory)
        
        self.scalemap = {}
        self.scales = []
        self.layers = []
        self.zoommap = {}
        self.zooms = []
        
        for s57path in fps.getfilePaths():
            s57 = ogrS57info.s57(s57path)
            
            scale = s57.getScale()
            self.scalemap[scale] = self.scalemap.get(scale, [])
            self.scalemap[scale].append(s57path)
            
            zoom = s57.getZoom()
            self.zoommap[zoom] = self.zoommap.get(zoom, [])
            self.zoommap[zoom].append(s57path)
            
            for lyr in s57.getLayerList():
                if self.layers.count(lyr) == 0:
                    self.layers.append(lyr)
 
        for key in self.scalemap.keys():
            self.scales.append(key)
            
        for key in self.zoommap.keys():
            self.zooms.append(key)
        
        self.scales.sort()
        self.zooms.sort()
    
    def getListOfZooms(self):
        return self.zooms
    
    def getFilesAtZoom(self, zoom):
        if self.zooms.count(int(zoom)) > 0:
            return self.zoommap[zoom]
    
    def getListOfScales(self):
        return self.scales
    
    def getFilesAtScale(self, scale):
        if self.scales.count(str(scale)) > 0:
            return self.scalemap[str(scale)]
        
    def getListOfLayers(self):
        return self.layers


if __name__ == "__main__":
    rootdir = "/home/will/zxyCharts/ENC_ROOT/REGION_15/ENC_ROOT"
    ss = s57Stats(rootdir)
    print ss.getFilesAtZoom(7)
    
 

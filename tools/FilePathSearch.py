#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

class FilePathSearch():
    def __init__(self, directory, extention="000", filter=None):
        """Searches for files ending in <extention> in <directory> and all subdirectories
           Optionally supply list of file names <filter> to only search for files in filter list
           Returns list of string paths"""
        self.extention = extention.upper()
        self.filePaths = []
        self.fileList = []
        self.filter = filter
        if os.path.exists(directory):
            self.__listFiles(directory)
        else:
            print directory, "is not a directory."
        
    def __mywalker(self, arg, dir, file):
        if self.filter == None:
            for f in file:
                sf = f.upper().split(".")
                ext = sf[len(sf)-1]
                if ext.upper().startswith(self.extention):
                    self.filePaths.append(dir+"/"+f)
                    self.fileList.append(f)
        else:
            for f in file:
                if f.upper().endswith(self.extention) and ( self.filter.count(f) > 0 ):
                    self.filePaths.append(dir+"/"+f)
                    self.fileList.append(f)
        
    def __listFiles(self, dir):
        os.path.walk(dir, self.__mywalker, None)
        
    def getfilePaths(self):
        return self.filePaths

if __name__== "__main__":
    dir = "/home/will/zxyCharts/ENC_ROOT/REGION_15/ENC_ROOT"
    filePathSearch = FilePathSearch(dir)
    for path in filePathSearch.getfilePaths():
        print path

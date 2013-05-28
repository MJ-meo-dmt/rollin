#!/usr/bin/python

from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters

#----------------------------------------------------------------------#

## CONFIG ##

class Config(DirectObject):
    
    def __init__(self, _main):
        self.main = _main
        
        ### BACKGROUND COLOR ###
        base.setBackgroundColor(0, 0, 0)
        
        #self.filters = CommonFilters(base.win, base.cam)
        #self.filters.setBloom(blend=(0.33, 0.33, 0.33,0), desat=0.0, intensity=1, size="small")
        
        
        ### SHADER SETTINGS ###
        render.setShaderAuto()
        #render.setAntialias(AntialiasAttrib.MLine)
        #render.setAttrib(LightRampAttrib.makeHdr2())
        
        
        ### CAMERA SETTINGS ###
        #self.lens = OrthographicLens()
        #self.lens.setFilmSize(20, 15)
        #base.cam.node().setLens(self.lens)

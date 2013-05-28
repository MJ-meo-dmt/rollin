#!/usr/bin/python

# System imports

# Panda Engine imports
from panda3d.rocket import *
from panda3d.core import TextNode

# Game imports

#----------------------------------------------------------------------#

class Gui():
    
    def __init__(self, _game):
        
        # Gui
        self.game = _game
        
        # load font
        LoadFontFace("gui/verdana.ttf")
        
        r = RocketRegion.make('pandaRocket', base.win)
        r.setActive(1)
        self.context = r.getContext()
        
        self.showMenu()
        
        # Input
        ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(ih)
        r.setInputHandler(ih)
        
    def hideMenu(self):
        
        self.menu.Close()
        
    def showMenu(self):
        
        self.menu = self.context.LoadDocument("gui/main.rml")
        self.menu.Show()
    
    def showGameGui(self):
        
        self.gameGui = self.context.LoadDocument("gui/game.rml")
        self.gameGui.Show()
    
    def hideGameGui(self):
        
        self.gameGui.Close()
        
    def setStyle(self, style):
        classToSet = self.gameGui.GetElementById('counter')
        classToSet.class_name = style
    
    def setCount(self, count):
        countText = self.gameGui.GetElementById('count')
        countText.inner_rml = str(count)
        
    
        
            


#!/usr/bin/python

# System imports

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject

# Game imports

#----------------------------------------------------------------------#

### GAME CORE ###

class Event():
    
    def __init__(self, _main):
        
        self.main = _main
        
    
    def doReset(self):
        self.main.restartLevel()
        
    def doChangeMovement(self, option):
        self.main.game.movementOption = option

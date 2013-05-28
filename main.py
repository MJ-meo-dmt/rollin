#!/usr/bin/python

# System imports
import sys

# Panda Engine imports
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Rollin
    fullscreen 0
    win-size 1024 768
    cursor-hidden 0
    sync-video 1
    show-frame-rate-meter 1

"""
)

from panda3d.rocket import *
from direct.showbase.ShowBase import ShowBase
# Game imports
from cfg import Config
from event import Event
from game import Game
#----------------------------------------------------------------------#

## Rollin ##

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # Load app configs
        self.config = Config(self)
        self.debug = False
        
        ## EVENT HANDLER ##
        self.event = Event(self)
        
        # Event keeper
        self.events = {
        "player-reset": self.event.doReset,
        "change-movement": self.event.doChangeMovement
        }
        
        # Accept Events
        for eventName in self.events.keys():
            self.accept(eventName, self.events[eventName])
            
        # Game.
        self.game = Game(self)  

        self.accept('escape', self.game.stopGame)
        


main = Main()
run()

## CURRENT PLAYABLE LEVELS ##
# 1. startLevel1
# 2. startLevel2
# 3. startLevel3
# Change them in game.py




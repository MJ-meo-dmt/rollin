#!/usr/bin/python

# System imports

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
# Game imports
from physics import Physics
from levelloader import LevelLoader
from input import Input
from player import Player
from camera import Camera
from weapon import Weapon
from gui import Gui
#----------------------------------------------------------------------#

### GAME CORE ###

class Game(DirectObject):
    
    def __init__(self, _main):
        
        self.main = _main
        
        ## PHYSICS HANDLER ##
        self.physics = Physics(self)
        
        ## LEVEL LOADER ##
        self.currentLevelName = None
        self.levelloader = LevelLoader(self)
        self.currentLevelName = "startLevel2-extra"
        
        ## INPUT HANDLER
        self.input = Input(self)
        self.movementOption = '1'
        
        ## HANDLE PLAYER ##
        self.isPlayerActive = False
        self.player = {}
        self.activePlayerName = "player2"
        
        ## Start GuI ##
        self.gui = Gui(self)
        
        self.accept("doStart", self.startGame)
        
        ## GAME STATE VARIABLES ##
        self.isMoving = False
        self.isFloating = False
    
    def startGame(self):
        self.gui.hideMenu()
        self.levelloader.newLevel(self.currentLevelName)
        self.createPlayer(self.activePlayerName)
        self.gui.showGameGui()
        self.levelloader.startCounter()
        
        ## HANDLE CAMERA ##
        self.camera = Camera(self)
        
        ## START PHYSICS ##
        self.physics.start()
        
    def stopGame(self):
        self.gui.hideGameGui()
        
        for object in self.levelloader.levelObjects:
            object.remove()
        
        for stateCoin in self.levelloader.levelStateCoins.keys():
            self.levelloader.levelStateCoins["exit"].exitModel.remove()
            self.levelloader.levelStateCoins["exit"] = None
            
        for coin in self.levelloader.levelCoins.keys():
            self.levelloader.levelCoins[coin].coinModel.remove()
            self.levelloader.levelCoins[coin] = None

        for node in self.physics.World.getRigidBodies():
            self.physics.World.removeRigidBody(node)
            
        for node in self.physics.World.getGhosts():
            self.physics.World.removeGhost(node)
            
        #self.levelloader.level = None
        self.levelloader.stopCounter()
        
        self.player[self.activePlayerName].removePlayer()
        self.player = None
        
        self.camera.stopCamTask()
        # Reset Cursor
        winProps = WindowProperties()
        winProps.setCursorHidden(False)
        base.win.requestProperties(winProps)
        self.camera = None
        
        self.physics.stop()
        
        self.gui.showMenu()
        
    
    def createPlayer(self, name):
        self.player = {}
        self.player[name] = Player(self, name)
        
        
        

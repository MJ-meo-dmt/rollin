#!/usr/bin/python

# System imports

# Panda Engine imports
from panda3d.bullet import *
from panda3d.core import *
from direct.particles.ParticleEffect import ParticleEffect

# Game imports

#----------------------------------------------------------------------#


# LevelPassCoins needed to continue to next level
class Coin():
    
    def __init__(self, _levelloader, coinCount, object, type):
        
        self.levelLoader = _levelloader
        
        # Setup
        radius = 0.45
        shape = BulletSphereShape(radius)
        
        node = BulletGhostNode(type+str(coinCount))
        #node.setMass(0)
        node.addShape(shape)
        
        self.coinNP = render.attachNewNode(node)
        self.coinNP.setPos(object.getPos())
        self.coinNP.setCollideMask(BitMask32(0x0f))
        
        
        self.coinModel = loader.loadModel("models/coin")
        self.coinModel.reparentTo(self.coinNP)
        #self.levelLoader.levelObjects.append(coinModel)
        
        self.levelLoader.physicsWorld.attachGhost(node)
        

class ExitCoin():
    
    def __init__(self, _levelloader, object, type):
        
        self.levelLoader = _levelloader
        
        # Setup
        radius = 0.48
        shape = BulletSphereShape(radius)
        
        node = BulletGhostNode(type)
        #node.setMass(0)
        node.addShape(shape)
        
        self.exitCoinNP = render.attachNewNode(node)
        self.exitCoinNP.setPos(object.getPos())
        self.exitCoinNP.setCollideMask(BitMask32(0x0f))
        
        self.exitModel = loader.loadModel("models/exit")
        self.exitModel.reparentTo(self.exitCoinNP)
        
        #self.levelLoader.levelObjects.append(exitModel)
        
        self.levelLoader.physicsWorld.attachGhost(node)
        
        




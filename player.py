#!/usr/bin/python

# System imports

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject
from panda3d.bullet import *
from panda3d.core import *
# Game imports

#----------------------------------------------------------------------#

class Player():
    
    def __init__(self, _game, name):
        
        self.game = _game
        
        # Start position
        self.startPos = self.game.levelloader.startPos
        self.physicsWorld = self.game.physics.World
        
        radius = 0.4
        shape = BulletSphereShape(radius)
        
        node = BulletRigidBodyNode("Player-"+name)
        node.setMass(1)
        node.addShape(shape)
        
        self.body = render.attachNewNode(node)
        self.body.setPos(self.startPos)
        self.body.setCollideMask(BitMask32.allOn())
        
        # Add player customize
        self.playerModel = loader.loadModel("models/"+name)
        self.playerModel.setScale(.65)
        self.playerModel.reparentTo(self.body)
      
        self.physicsWorld.attachRigidBody(node)
        
        # Nothing for this yet
        self.game.isPlayerActive = True
        
        # For the picker ray. dont think this is needed anymore.
        # but its working just fine so id rather leave it :P
        playerRayNode = self.playerModel.attachNewNode("ray-dummy")
        playerRayNode.setCompass()
        self.playerRayNode = playerRayNode
    
    def removePlayer(self):
        self.playerModel.remove()
        self.physicsWorld.remove(self.body.node())
        self.body.removeNode()

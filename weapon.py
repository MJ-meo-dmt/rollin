#!/usr/bin/python

from panda3d.core import *
from pandac.PandaModules import *
from panda3d.bullet import *
from direct.showbase.DirectObject import DirectObject

#----------------------------------------------------------------------#

## Weapons ##

class Weapon(DirectObject):
    
    def __init__(self, _game):
        
        self.game = _game
        
        self.activeBullets = []
        self.physicsWorld = self.game.physics.World
        
        self.accept("mouse1", self.fireBullet, [ccd])
    
    def removeBullet(self, task):
        
        if len(self.activeBullets) < 1:return
        
        bulletNP = self.activeBullets.pop(0)
        self.physicsWorld.removeRigidBody(bulletNP.node())
        
        return task.done
        
    def fireBullet(self, ccd):
        
        pMouse = base.mouseWatcherNode.getMouse()
        pFrom = Point3()
        pTo = Point3()
        base.camLens.extrude(pMouse, pFrom, pTo)
        
        pFrom = render.getRelativePoint(base.cam, pFrom)
        pTo = render.getRelativePoint(base.cam, pTo)
        
        v = pTo = pFrom
        v.normalize()
        v *= 10000.0
        
        # Create the bullet
        shape = BulletBoxShape(Vec3(.5, .5, .5))
        body = BulletRigidBodyNode('Bullet')
        bodyNP = render.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.node().setMass(2.0)
        bodyNP.node().setLinearVelocity(Vec3(v))
        bodyNP.setPos(pFrom)
        bodyNP.setCollideMask(BitMask32.allOn())
        
        model = loader.loadModel("models/box")
        model.reparentTo(bodyNP)
        
        print body
        
        # Enable CCD
        bodyNP.node().setCcdMotionThreshold(1e-7)
        bodyNP.node().setCcdSweptSphereRadius(0.50)
        
        self.physicsWorld.attachRigidBody(bodyNP.node())
        
        self.activeBullets.append(bodyNP)
        taskMgr.doMethodLater(2, self.removeBullet, "removeBullet")

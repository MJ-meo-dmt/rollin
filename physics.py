#!/usr/bin/python

# System imports

# Panda Engine imports
from panda3d.bullet import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject

# Game imports

#----------------------------------------------------------------------#

class Physics(DirectObject):
    
    def __init__(self, _game):
        
        self.game = _game
        
        ### BASE PHYSICS WORLD ###
        self.World = BulletWorld()
        self.World.setGravity(Vec3(0, 0, -9))
        
        if self.game.main.debug:
            self.enableDebug()
        else:
            pass
    
    def enableDebug(self):
        
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()
        self.World.setDebugNode(debugNP.node())
        
    def movement(self):
        ## GET PLAYER BODY ##
        self.playerBody = self.game.player[self.game.activePlayerName].body
        
        speed = Vec3(0, 0, 0)
        jump = Vec3(0, 0, 0)
        
        if self.game.movementOption == '1':
            if inputState.isSet('left'):
                #self.checkFloorCollide()
                speed.setX(-3.0)
            
            if inputState.isSet('right'):
                #self.checkFloorCollide()
                speed.setX(3.0)
            
            if inputState.isSet('up'):
                speed.setY(3.0)
                
            if inputState.isSet('down'):
                speed.setY(-3.0)
        
            if inputState.isSet('space'):
            
                self.checkFloorCollide()
                if self.game.isFloating != True:
                    jump.setZ(0.9)
                    self.game.isFloating = True
                elif self.game.isFloating == True:
                    jump.setZ(0.0)
                    #self.game.isFloating = False
                    
        if self.game.movementOption == '2':
            if inputState.isSet('left'):
                #self.checkFloorCollide()
                speed.setY(3.0)
            
            if inputState.isSet('right'):
                #self.checkFloorCollide()
                speed.setY(-3.0)
            
            if inputState.isSet('up'):
                speed.setX(3.0)
                
            if inputState.isSet('down'):
                speed.setX(-3.0)
        
            if inputState.isSet('space'):
            
                self.checkFloorCollide()
                if self.game.isFloating != True:
                    jump.setZ(0.9)
                    self.game.isFloating = True
                elif self.game.isFloating == True:
                    jump.setZ(0.0)
                    #self.game.isFloating = False
                    
        if self.game.movementOption == '3':
            if inputState.isSet('left'):
                #self.checkFloorCollide()
                speed.setY(-3.0)
            
            if inputState.isSet('right'):
                #self.checkFloorCollide()
                speed.setY(3.0)
            
            if inputState.isSet('up'):
                speed.setX(-3.0)
                
            if inputState.isSet('down'):
                speed.setX(3.0)
        
            if inputState.isSet('space'):
            
                self.checkFloorCollide()
                if self.game.isFloating != True:
                    jump.setZ(0.9)
                    self.game.isFloating = True
                elif self.game.isFloating == True:
                    jump.setZ(0.0)
                    #self.game.isFloating = False
                    
                    
        if self.game.movementOption == '4':
            if inputState.isSet('left'):
                #self.checkFloorCollide()
                speed.setX(3.0)
            
            if inputState.isSet('right'):
                #self.checkFloorCollide()
                speed.setX(-3.0)
            
            if inputState.isSet('up'):
                speed.setY(-3.0)
                
            if inputState.isSet('down'):
                speed.setY(3.0)
        
            if inputState.isSet('space'):
            
                self.checkFloorCollide()
                if self.game.isFloating != True:
                    jump.setZ(0.9)
                    self.game.isFloating = True
                elif self.game.isFloating == True:
                    jump.setZ(0.0)
                    #self.game.isFloating = False
        
        self.playerBody.node().setActive(True)
        self.playerBody.node().applyCentralForce(speed)
        self.playerBody.node().applyCentralImpulse(jump)
    
    def checkFloorCollide(self):
        # Get player pos
        pos = Point3(self.game.player[self.game.activePlayerName].playerRayNode.getPos(render))
        
        pFrom = Point3(pos)
        pTo = Point3(float(pos.getX()), float(pos.getY()),float(pos.getZ()-0.7))
        
        result = self.World.rayTestClosest(pFrom, pTo)
        contactNode = result.getNode()
        
        if contactNode == None:
            self.game.isFloating = True
            
        elif contactNode in self.game.levelloader.jumpFrom:
            self.game.isFloating = False
            
    
    def checkPlayerCoinCollide(self):
        
        result = self.World.contactTest(self.game.player[self.game.activePlayerName].body.node())
        
        for contact in result.getContacts():
            if contact.getNode1() in self.World.getGhosts():
                ghost = contact.getNode1()
                ghostNP = NodePath(ghost)
                ghostStringName = str(ghostNP)
                ghostfinalString = ghostStringName[7:]
                
                if ghostfinalString == "exit":
                    print "Exit now!!!!"
                    self.World.removeGhost(ghost)
                    self.game.levelloader.levelStateCoins[ghostfinalString].exitCoinNP.removeNode()
                    
                else:
                    self.game.levelloader.levelCoins[ghostfinalString].coinNP.removeNode()
                    self.game.levelloader.coinCount -= 1
                    self.World.removeGhost(ghost)


    def update(self, task):
        
        dt = globalClock.getDt()
        self.World.doPhysics(dt, 5, 1.0/240.0)
        self.movement()
        self.checkPlayerCoinCollide()

        return task.cont
    
    
    def start(self):
        
        taskMgr.add(self.update, "update-physics", priority=1)
    
    def stop(self):
        
        taskMgr.remove("update-physics")
    
        

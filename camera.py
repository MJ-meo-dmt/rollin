#!/usr/bin/python

from panda3d.core import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject
#----------------------------------------------------------------------#

## Camera ##

class Camera(DirectObject):
    
    def __init__(self, _game):
        
        self.game =_game
        
        ## Player cam node
        self.playerCamNode = self.game.player[self.game.activePlayerName].body.attachNewNode("cam-dummy")
        self.playerCamNode.setCompass()
        
        
        taskMgr.add(self.camTask, "cam-task")
        
        base.camera.reparentTo(self.playerCamNode)
        #base.camera.lookAt(self.playerCamNode)
        # Temp place
        self.controlMap = {"wheel_up": 0, "wheel_down": 0}
        self.accept("wheel_up", self.setControl, ["wheel_up", 1])
        self.accept("wheel_down", self.setControl, ["wheel_down", 1])
        
        self.cameraZ = 2.5
        self.cameraDistance = 40
        self.cameraPitch = 10
        self.cameraHead = 100
        #base.disableMouse()
        self.followCam()
        
        winProps = WindowProperties()
        winProps.setCursorHidden(True)
        base.win.requestProperties(winProps)
    
        
    def stopCamTask(self):
        taskMgr.remove("cam-task")    
    
    def setControl(self, key, value):
        self.controlMap[key] = value
    
    def camTask(self, task):
        
        player = self.game.player[self.game.activePlayerName].body
        playerX = player.getX()
        playerY = player.getY()
        playerZ = player.getZ()
        
        if (self.controlMap["wheel_up"] != 0):
            self.cameraDistance -= 0.1 * self.cameraDistance
            if (self.cameraDistance < 3):
                self.cameraDistance = 3
            self.controlMap["wheel_up"] = 0
            
        elif (self.controlMap["wheel_down"] != 0):
            self.cameraDistance += 0.1 * self.cameraDistance
            if (self.cameraDistance > 100):
                self.cameraDistance = 100
            self.controlMap["wheel_down"] = 0
            
            
        # Check cam positions:
        
        if self.game.movementOption == "1":
            self.playerCamNode.setPos(0, (playerY - 10), self.cameraZ)
            base.camera.setY(self.playerCamNode, -self.cameraDistance)
            self.game.gui.setStyle("style1")
            
        if self.game.movementOption == "2":
            self.playerCamNode.setPos((playerX - 5), 0, self.cameraZ)
            base.camera.setX(self.playerCamNode, -self.cameraDistance)
            base.camera.lookAt(self.playerCamNode)
            self.game.gui.setStyle("style2")
        
        if self.game.movementOption == "3":
            self.playerCamNode.setPos((playerX + 10), 0, self.cameraZ)
            base.camera.setX(self.playerCamNode, self.cameraDistance)
            base.camera.lookAt(self.playerCamNode)
            self.game.gui.setStyle("style3")
        
        if self.game.movementOption == "4":
            self.playerCamNode.setPos(0, (playerZ + 5), self.cameraZ)
            base.camera.setY(self.playerCamNode, self.cameraDistance)
            base.camera.lookAt(self.playerCamNode)
            self.game.gui.setStyle("style4")
            
        
        #if base.mouseWatcherNode.hasMouse():
            
           # md = base.win.getPointer(0)
            #x = md.getX()
            #y = md.getY()
        
            
            #deltaX = md.getX() - 200
            #deltaY = md.getY() - 200
            
            #base.win.movePointer(0, 200, 200)
            
            
            #mouseSpeed = 3.0
            
            #self.cameraHead = self.cameraHead + 0.05 * deltaX
            
            #if (self.cameraHead < -360): self.cameraHead = -360
            #if (self.cameraHead > 360): self.cameraHead = 360
            
            #self.cameraPitch = self.cameraPitch - 0.05 * deltaY
            
            #if (self.cameraPitch < 0): self.cameraPitch = 0
            #if (self.cameraPitch > 85): self.cameraPitch = 85
            
            #base.camera.setPos(0, 0, self.cameraTargetHeight/2)
            #base.camera.setHpr(self.cameraHead, self.cameraPitch, 0)
        
        

        #view = Point3(0, 0, self.cameraTargetHeight)
        #base.camera.lookAt(view)
           
        
        return task.cont
            
            
            
        
    
    def followCam(self):
        
        base.camera.reparentTo(self.playerCamNode)
        base.camera.lookAt(self.playerCamNode)
        
        

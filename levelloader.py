#!/usr/bin/python

# System imports

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from panda3d.bullet import *
from direct.task.Task import Task

# Game imports
from coins import *
#----------------------------------------------------------------------#

class LevelLoader():
    
    def __init__(self, _game):
        
        self.game = _game
        
        ## PHYSICS WORLD ##
        self.physicsWorld = self.game.physics.World
        
        # Object types in levels
        self.objectTypes = ["floor", "box", "light", "coin", "exit", "start", "level"]
        
        # Counters
        self.boxCount = 0
        self.coinCount = 0
        self.levelCount = 0
        self.startPos = (0, 0, 0)#(-10.0, 0, 0.8)
        
        
        # For collison checking for jump
        self.jumpFrom = []
        
        ## COIN TYPES ##
        # State coins are Start and Exit coins, maybe portal coins aswell
        self.levelStateCoins = {}
        # Pass coints are coins needed to continue.
        self.levelCoins = {}
        # Hold level sensors
        self.levelSensors = {}
        
        self.levelObjects = []
    
    def startCounter(self):
        
        taskMgr.add(self.coinCounterTask, "counterTask", priority=3)
    
    def coinCounterTask(self, task):
        self.count = self.coinCount
        self.game.gui.setCount(self.count)
        
        return task.cont
    
    def stopCounter(self):
        taskMgr.remove("counterTask")
        
        
    def newLevel(self, levelName):
        
        # Add ambient light
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        
        # parse the level for setup
        
        self.level = loader.loadModel("models/"+levelName)
        
        # Find all objects
        self.objects = self.level.findAllMatches('**')
        
        for object in self.objects:
            for type in self.objectTypes:
                if object.hasTag(type):
                    self.setupLevel(object, type, self.level)
                    
    
    def setupLevel(self, object, type, levelModel):
        
        # Setup base floor
        if type == "floor":
            
            shape = BulletPlaneShape(Vec3(0, 0, 0.1), 1)
            node = BulletRigidBodyNode('floor')
            node.addShape(shape)
            np = render.attachNewNode(node)
            np.setPos(0, 0, -1)
            np.setCollideMask(BitMask32.allOn())
            self.physicsWorld.attachRigidBody(node)
            object.reparentTo(np)
            object.setPos(0, 0, 1)
            
            self.jumpFrom.append(node)
            self.levelObjects.append(object)
            
        if type == "level":
            self.levelCount += 1
            tmpMesh = BulletTriangleMesh()
            node = object.node()
            
            if node.isGeomNode():
                tmpMesh.addGeom(node.getGeom(0))
            else:
                return
                
            body = BulletRigidBodyNode('level'+str(self.levelCount))
            body.addShape(BulletTriangleMeshShape(tmpMesh, dynamic=False))
            body.setMass(0)
            
            np = render.attachNewNode(body)
            np.setCollideMask(BitMask32.allOn())
            np.setScale(object.getScale(levelModel))
            np.setPos(object.getPos(levelModel))
            np.setHpr(object.getHpr(levelModel))
            
            #object.setScale(np.getScale(levelModel))
            #object.setPos(render, np.getPos(levelModel))
            
            if object.hasTag("invis"):
                pass
            else:
                object.reparentTo(render)
            
            self.physicsWorld.attachRigidBody(body)
            
            self.jumpFrom.append(body)
            self.levelObjects.append(object)
                
            
        if type == "box":
            self.boxCount += 1
            shape = BulletBoxShape(Vec3(.8, .8, .8))
            node = BulletRigidBodyNode('box-'+str(self.boxCount))
            node.addShape(shape)
            
            if object.hasTag("dynamic"):
                node.setMass(int(object.getTag("dynamic")))
            else:
                pass
            
            np = render.attachNewNode(node)
            np.setCollideMask(BitMask32.allOn())
            np.setPos(object.getPos(levelModel))
            np.setHpr(object.getHpr())
            #object.reparentTo(np)
            #object.setScale(.8, .8, .8)
            self.physicsWorld.attachRigidBody(node)
            
            self.jumpFrom.append(node)
            
            boxModel = loader.loadModel("models/box")
            boxModel.setScale(.8, .8, .8)
            boxModel.reparentTo(np)
            self.levelObjects.append(object)
            self.levelObjects.append(boxModel)
            
        if type == "light":
            
            if object.getTag("light") == "point":
                plight = PointLight('plights')
                plight.setColor(VBase4((float(object.getTag('r')), 
                    float(object.getTag('g')), float(object.getTag('b')), 1)))
                
                #plight.setShadowCaster(True, 512, 512)
                plight.setAttenuation(Point3(0, 0, 0.1))
                plnp = render.attachNewNode(plight)
                plnp.setPos(object.getPos())
                render.setLight(plnp)
                self.levelObjects.append(object)
                self.levelObjects.append(plnp)
            
            if object.getTag("light") == "spot":
                slight = Spotlight('slights')
                slight.setColor(VBase4(float(object.getTag('r')), 
                    float(object.getTag('g')), float(object.getTag('b')), 1))
                lens = PerspectiveLens()
                slight.setLens(lens)
                slight.setAttenuation(Point3(0, 0, 0.1))
                #slight.setShadowCaster(True, 256, 256)
                slnp = render.attachNewNode(slight)
                slnp.setPos(object.getPos())
                lookatName = object.getTag("lookat")
                slnp.lookAt(levelModel.find("**/"+lookatName))
                render.setLight(slnp)
                self.levelObjects.append(object)
                self.levelObjects.append(slnp)
            
            
        if type == "start":
            self.startPos = object.getPos(levelModel)
            self.levelObjects.append(object)
        if type == "exit":
            self.levelStateCoins[type] = ExitCoin(self, object, type)
            
        if type == "coin":
            self.coinCount += 1
            self.levelCoins[type+str(self.coinCount)] = Coin(self, 
                                self.coinCount, object, type)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

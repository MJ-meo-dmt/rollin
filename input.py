#!/usr/bin/python

# System imports

# Panda Engine imports
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
# Game imports

#----------------------------------------------------------------------#

class Input(DirectObject):
    
    def __init__(self, _game):
        
        
        # Reset Player
        self.accept('r', self.msgPlayerReset)
        
        # Change movement axis
        self.accept('1', self.msgChangeMovement, ['1'])
        self.accept('2', self.msgChangeMovement, ['2'])
        self.accept('3', self.msgChangeMovement, ['3'])
        self.accept('4', self.msgChangeMovement, ['4'])
        
        
        ## MOVEMENT INPUTS ##
        inputState.watchWithModifiers('up', 'w')
        inputState.watchWithModifiers('down', 's')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('space', 'space')
        #Check jump
        #self.accept("space", self.doJump)

    
    
    
    
    ### EVENT MSGS ###
    def msgPlayerReset(self):
        base.messenger.send("player-reset")
    
    def msgChangeMovement(self, option):
        base.messenger.send("change-movement", [option])

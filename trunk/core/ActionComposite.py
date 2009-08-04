from SessionAction import SessionAction
from SessionStatus import SessionStatus
import copy
class ActionComposite(SessionAction):
    def __init__(self, sessionActions = None):
        SessionAction.__init__(self)
        self.sessionActions = []
        self.canceled = False
        
    def init(self):
        for action in self.sessionActions:  
            action.init()
        return False
    
    def setup(self):
        for action in self.sessionActions:
            if self.isCancel() == True:
                break
            action.setup()
        self.canceled = False
        return False
    
    def play(self):
        for action in self.sessionActions:
            action.play()
        return False
    
    def pause(self):
        for action in self.sessionActions:  
            action.pause()
        return False

    def stop(self):
        for action in self.sessionActions:  
            action.stop()
        return True
    
    def updateStatus(self):
        ishasAlive = 0
        for action in self.sessionActions:  
            ishasAlive |= action.updateStatus()
        return False
    
    def remove(self):
        removedActions = []
        for action in self.sessionActions:  
            if action.remove():
                removedActions.append(action)
                
        for action in removedActions:
            self.sessionActions.remove(action)
            
        return False
    
    def addAction(self, action):
        self.sessionActions.append(action)
    
    def removeAction(self, action):
        self.sessionActions.remove(action)
        
    def cancel(self):
        self.canceled = True
        
    def isCancel(self):
        return self.canceled
    
    def doAction(self, op):
        action = actionsMap[op]
        action()
    
    def clear(self):
        self.sessionActions = []
        return False
  
            
    
    
    
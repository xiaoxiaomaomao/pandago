
class SessionAction:
    OP_DUMMY = 0
    OP_STOP = 1 << 0
    OP_SETUP = 1 << 1 
    OP_PLAY = 1 << 2
    OP_PAUSE = 1 << 3
    OP_REMOVE = 1 << 4
    
    #MUST set it to the biggest value in all status values.
    #Because update status operation want to check the session's status
    #if don't set it to the biggest value,it will ignore latest status
    #that maybe cause session group thread think there is not alive session and exit
    #See SessionGroup run method.
    OP_UPDATE_STATUS = 1 << 5 
    MASK = 6
    def __init__(self):
        self.actionMap = {SessionAction.OP_DUMMY    : self.dummy,\
                          SessionAction.OP_STOP     : self.stop,\
                          SessionAction.OP_PLAY     : self.play,\
                          SessionAction.OP_SETUP    : self.setup,\
                          SessionAction.OP_UPDATE_STATUS : self.updateStatus,\
                          SessionAction.OP_REMOVE   : self.remove,\
                          SessionAction.OP_PAUSE    : self.pause,\
                          }
        
    def __getitem__(self, key):
        return self.actionMap[key]
    
    def init(self):
        return False
    
    def stop(self, param = None):    
        return False
    
    def play(self, param = None):
        return False
    
    def setup(self, param = None):
        return False

    def pause(self, param = None):
        return False
    
    def updateStatus(self, param = None):
        return False
    
    def remove(self, param = None):
        return False
    
    def dummy(self, param = None):
        return False
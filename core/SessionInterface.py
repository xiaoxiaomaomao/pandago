#!/usr/bin/python
class SessionInterface:
    def getStatus(self):
        pass

    def getTime(self, param = None):
        pass
    
    def stop(self, param = None):
        pass

    def play(self, param = None):
        pass
    
    def getParamsFromRemote(self, dic):
        pass

    def keepAlive(self):
        pass
    
    def getPacketData(self):
        pass
    
    def setup(self, address):
        pass
    
    def getErrorInfo(self):
        pass

    def getLocalPort(self):
        pass

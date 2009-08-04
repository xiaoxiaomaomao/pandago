from Observer import Observer
from Filter import Filter
class Monitor(Observer):
    CAPTURE_PACKET  = 0x10
    CONTROL_SESSION = 0x20
    def __init__(self, type = CAPTURE_PACKET):
        self.filter = None
        self.type = type
        
    def updateView(self, viewData):
        pass
    
    def setFilter(self, filter):
        self.filter = filter
        
    def doFilter(self, rawData):
        packetData = rawData
        if self.filter != None:
             packetData = self.filter.doFilter(rawData)
        return packetData
    
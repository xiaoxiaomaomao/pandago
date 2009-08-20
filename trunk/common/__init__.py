import sys
GROUP_SIZE = 2

def createSession(protocol, address, param, number, manager, view, monitorClass = None, groupSize = GROUP_SIZE,startingPoint = 0):
        groupsNum = number / groupSize
        index = startingPoint
        for i in xrange(0, groupsNum):
            group = manager.createSessionGroup(protocol,view)
            for i in xrange(0, groupSize):
                if monitorClass != None:
                    group.addSession(address.replace('*', str(index)), param, monitorClass(manager))
                else:
                    group.addSession(address.replace('*', str(index)), param, None)
                index += 1

        if number % groupSize >= 0:
            group = manager.createSessionGroup(protocol,view)
            for i in xrange(0, number % groupSize):
                if monitorClass != None:
                    group.addSession(address.replace('*', str(index)), param, monitorClass(manager))
                else:
                    group.addSession(address.replace('*', str(index)), param, None)
                index += 1


CONFIG_FILE_IS_NOT_EXIST = -1
CONFIG_FILE_HAVE_ERROR = -2
NO_ERROR = 0
class Config:
    def __init__(self):
        self.address  = None
        self.number   = None
        self.param    = None
        self.protocol = None

import ConfigParser
import os
def readConfigFromFile(path):
    parser = ConfigParser.ConfigParser()
    config = Config()
    try:
        if os.path.isfile(path) == False:
            return None
            
        parser.read(path)
        sessions = parser.sections()
        for session in sessions:
            config.address  = parser.get(session, 'Address')
            config.number   = int(parser.get(session, 'Number'))
            config.param    = parser.get(session, 'Param')
            config.protocol = parser.get(session, 'Protocol')
            
    except:
        return None
        
    return config
    

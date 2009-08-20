#!/usr/bin/python
class SessionStatus:
    INITIAL  = 1 << 0
    CONNECTING = 1 << 1 
    RUNNING  = 1 << 2
    PAUSE = 1 << 3
    STOPPED = 1 << 4
    SETUP = 1 << 5
    NETWORKERROR = 1 << 10
    PROTOCOLERROR = 1 << 11
    EXECPTION = 1 << 12
    REMOVED = 1 << 13
    def __init__(self,session = None):
        self.time = 0
        self.address = None
        self.status = SessionStatus.INITIAL
        self.session = session
        self.type = "NULL"
        self.id = 0
        self.param = None
        self.paramsFromRemote = None
        self.packetData = None
        self.session = None
        self.errorInfo = ""
        self.localPort = ""
        
    def setParam(self,param):
        self.param = param

    def getParam(self):
        return self.param

    def getAddress(self):
        return self.address
    
    def setAddress(self,address):
        self.address = address

    def getSession(self):
        return self.session

    def getTime(self):
        return self.time
    
    def getStatus(self):
        return self.status
    
    def getProtocol(self):
        return self.type
    
    def setProtocol(self, type):
        self.type = type

    def setTime(self,time):
        self.time = time

    def setStatus(self, status):
        self.status = status
        
    def setId(self,id):
        self.id = id
    
    def getId(self):
        return self.id

    def setParamsFromRemote(self, dic):
        self.paramsFromRemote = dic

    def getParamsFromRemote(self):
        return self.paramsFromRemote
    
    def getPacketData(self):
        return self.packetData
    
    def setPacketData(self, data):
        self.packetData = data
    
    def setSession(self, session):
        self.session = session
    
    def getSession(self):
        return self.session
    
    def setErrorInfo(self, info):
        self.errorInfo = info
    
    def getErrorInfo(self):
        return self.errorInfo
    
    def setLocalPort(self, port):
        self.localPort = port

    def getLocalPort(self):
        return self.localPort

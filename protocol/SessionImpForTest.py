#!/usr/bin/python
import sys
import ctypes
import threading
import random
import time
from core import SessionImp
from core.SessionStatus import SessionStatus

class SessionImpForTest(SessionImp.SessionImp):
    def __init__(self):
        self.status = SessionStatus.INITIAL
        self.time = 0
        self.paused = False
        self.statusMap = {SessionStatus.RUNNING:"Running", SessionStatus.STOPPED:"Stopped", SessionStatus.INITIAL:"Initial",\
                SessionStatus.CONNECTING:"Connecting", SessionStatus.NETWORKERROR:"Failed", SessionStatus.EXECPTION:"Execption",\
                SessionStatus.REMOVED:"orange",\
                SessionStatus.PAUSE: "Pause"}
        self.random = [SessionStatus.RUNNING,SessionStatus.STOPPED,SessionStatus.NETWORKERROR, SessionStatus.EXECPTION]
        self.prevTime = -1
        self.detectExceptTimes = 0

    def setup(self, address, param):
        self.time = 0
        self.status = SessionStatus.SETUP
        self.detectExceptTimes = 0
        return SessionStatus.SETUP
    
    def play(self, param = None):
        self.status = SessionStatus.RUNNING
        return self.status
    
    def stop(self, param = None):
        self.status = SessionStatus.STOPPED
        
    def pause(self, param = None):
        if self.paused:
            self.status = SessionStatus.RUNNING
            self.paused = False
        else:
            self.status = SessionStatus.PAUSE
            self.paused = True
        
    def getStatus(self):
        return self.status 
    
    def getTime(self):
        return self.time

    def keepAlive(self):
        self.time += 1
        if self.time > 5:
            self.status =  SessionStatus.NETWORKERROR
            return SessionStatus.NETWORKERROR
       
    def getErrorInfo(self):
        return "fails"
    
    def getPacketData(self):
        return "Packet:IP:192.168.0.251 RTSP Time "

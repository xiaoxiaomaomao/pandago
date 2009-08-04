#!/usr/bin/python

from SessionGroup import SessionGroup
import SessionStatus
import SessionStatistics
import threading
from SessionAction import SessionAction
""" Manager the  test session """
class SessionManager:
    def __init__(self):
        self.sessionGroups = []
        self.mutex = threading.Lock()
        self.observers = []
        self.sessionGroupsId = 0
        self.statics = SessionStatistics.SessionStatistics()
        
    def createSessionGroup(self, protocol, observer):
        group = SessionGroup(self.sessionGroupsId, protocol, observer)
        self.sessionGroups.append(group)
        return group
    
    def registerObserver(self, group, observer):
        if group in self.sessionGroups:
            group.registerObserver(observer)
            
    def unregisetrObserver(self, group, observer):
        if group in self.sessionGroups:
            group.unregisetrObserver(None)
            
    def clear(self, param = None, ids = None):
        removedGroup = []
        for group in self.sessionGroups:
            if group.remove():
                removedGroup.append(group)
        for group in removedGroup:
            self.sessionGroups.remove(group)

    def play(self, ids = None, param = None):
        for group in self.sessionGroups:
            self.__helper(group.play, group.doActionByID, SessionAction.OP_PLAY, ids, param)
    
    def setup(self, ids = None, param = None):
        for group in self.sessionGroups:
            self.__helper(group.setup, group.doActionByID, SessionAction.OP_SETUP, ids, param)
            
    def stop(self, ids = None, param = None):  
        for group in self.sessionGroups:
            self.__helper(group.stop, group.doActionByID, SessionAction.OP_STOP, ids, param)
    
    def pause(self, ids = None, param = None):
        for group in self.sessionGroups:
            self.__helper(group.pause, group.doActionByID, SessionAction.OP_PAUSE, ids, param)
            
    def forceStop(self):
        for group in self.sessionGroups:
            group.forceStop()
    
    def registerMonitor(self, monitor, id):
        for group in self.sessionGroups:
            group.registerMonitor(monitor, id)
    
    def unregisterMonitor(self, monitor, id):
        for group in self.sessionGroups:
            group.unregisterMonitor(monitor, id)
            
    def getStatistics(self):
        self.statics.clear()
        for group in self.sessionGroups:
            s = group.getStatistics()
            self.statics += s

        return self.statics

    def __helper(self, action1, action2, op, ids = None, param = None):
        if ids == None:
            action1(param)
        else:
            action2(op, param, ids)
             

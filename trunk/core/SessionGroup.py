#!/usr/bin/python

import thread
import time
import SessionStatistics
from Observer import Observer
from Subject import Subject
from SessionStatus import SessionStatus
from SessionInterface import SessionInterface
from SessionAction import SessionAction
from SessionFactory import SessionFactory
from ActionComposite import ActionComposite
from Session import Session


UPDATE_TIME = 1
INVALID_SESSION_ID = -1
sessionId = INVALID_SESSION_ID

"""Represent a Protocol session"""
class SessionGroup(Subject, Observer):
    """
        Construct function.
        @param id the id of session
        @param the protocol address
        @param the concrete implementation of protocol
    """
    def __init__(self, groupId, protocol, observer):
        self.listeners = []
        self.lockForSessions = thread.allocate_lock()
        self.sessions = []
        self.IDs = []
        self.protocol = protocol
        self.groupId = groupId
        self.opSelector = SessionAction.OP_DUMMY
        self.actionsToRun = []
        
        self.lockForRunning = thread.allocate_lock()
        self.running = False
        self.stopped = False
        
        self.statics = SessionStatistics.SessionStatistics()
        self.actionsComposite = ActionComposite()
        
        self.observer = observer
        
    def __addSession(self, address, param, sessionId, monitor):
        status = SessionStatus()
        status.setId(sessionId)
        status.setProtocol(self.protocol)
        status.setParam(param)
        status.setAddress(address)
        self.IDs.append(sessionId)
        
        imp = SessionFactory.createSession(self.protocol)
        self.lockForSessions.acquire()
        session = Session(imp, status)
        status.setSession(session)
        session.registerObserver(self)#SessionGroup as the observer of session.
        session.registerMonitor(monitor)
        session.init()
        self.sessions.append(session)
        self.actionsComposite.addAction(session)
        self.lockForSessions.release()
        
    def addSession(self, address, param, monitor = None):
        global sessionId
        sessionId += 1
        self.__addSession(address, param, sessionId, monitor)

    def addSessionWithID(self, address, param, sessionId, monitor = None):
        self.__addSession(address, param, sessionId, monitor)
    
    def registerObserver(self, observer):
        self.observer = observer
    
    def unregisetrObserver(self, observer):
        self.observer = None
        
    def runForSpecifyAction(self):
        self.lockForSessions.acquire()
        actions = self.actionsToRun
        self.actionsToRun = []
        self.lockForSessions.release()

        for action in actions:
            doAction, paramter = action
            doAction(paramter)

    def runForEverySession(self):
        selector = self.opSelector
        mask = 1
        actions = []

        self.lockForSessions.acquire()
        for i in range(0, SessionAction.MASK):
            action = self.actionsComposite[selector & mask]
            actions.append(action)
            mask = mask << 1
        self.lockForSessions.release()
        
        self.opSelector ^= selector
        self.opSelector |= SessionAction.OP_UPDATE_STATUS
            
        for doAction in actions:
            self.stopped |= doAction()
         
    def run(self):
        self.lockForRunning.acquire()
        self.stopped = False
        while self.stopped != True:
            self.runForSpecifyAction()
            self.runForEverySession()
            time.sleep(UPDATE_TIME)
        action = self.actionsComposite[SessionAction.OP_UPDATE_STATUS]
        action()
        self.lockForRunning.release()
        
    def remove(self):
        self.opSelector |= SessionAction.OP_REMOVE
        if self.lockForRunning.locked() == False:
            action = self.actionsComposite[SessionAction.OP_REMOVE]
            action()
        return False
    
    def getStatistics(self):
        self.statics.clear()
        for session in self.sessions:
            self.statics[session.getStatus().getStatus()] += 1
        return self.statics
    
    def pause(self, param):
        self.opSelector |= SessionAction.OP_PAUSE
        
    def stop(self, param):
        if self.opSelector == SessionAction.OP_PLAY:
            self.actions.cancel()
    
        self.opSelector |= SessionAction.OP_STOP
    
    def play(self, param):
        #call it only when the session group is inactive
        self.opSelector |= SessionAction.OP_PLAY
    
    def __createThread(self):
        if self.lockForRunning.locked() == False or self.stopped == True:
            thread.start_new_thread(self.run, ())
           
    def setup(self, param):
        self.opSelector |= SessionAction.OP_SETUP
        self.__createThread()
        
    def forceStop(self):
        self.opSelector = SessionAction.OP_STOP
        self.lockForSessions.acquire()
        stopAction = self.actionsComposite[SessionAction.OP_STOP]
        stopAction()
        self.lockForSessions.release()
                 
    def __filterMemberID(self, ids):
        self.lockForSessions.acquire()
        memberIDs = set(self.IDs) & set(ids)
        self.lockForSessions.release() 
        return memberIDs
    
    def doActionByID(self, op, param, ids):
        memberIDs = self.__filterMemberID(ids)
        if len(memberIDs) <= 0:
            return False
        self.__gatherActions(op, param, memberIDs)
        self.__createThread()
        return 
    
    def __gatherActions(self, op, param, ids):
        self.lockForSessions.acquire()
        for session in self.sessions:
            status = session.getStatus()
            if status.getId() in ids:
                self.actionsToRun.append((session[op], param))
        self.lockForSessions.release()      
            
    def __isMember(self, id):
        return id in self.IDs
    
    def __findSession(self, id):
        self.lockForSessions.acquire()
        if self.__isMember(id):
            for session in self.sessions:
                status = session.getStatus()
                if status.getId() == id:
                    self.lockForSessions.release()
                    return session
        self.lockForSessions.release()
        return None
    
    def registerMonitor(self, monitor, id):
        session = self.__findSession(id)
        if session != None:
            session.registerMonitor(monitor)

    def unregisterMonitor(self, monitor, id):
        if self.__isMember(id):
            for session in self.sessions:
                session.unregisterMonitor(monitor)

    def updateView(self, sessionInfo):
        status = sessionInfo.getStatus()
        if status == SessionStatus.REMOVED:
            self.sessions.remove(sessionInfo.getSession())
        
        if self.observer != None:
            self.observer.updateView(sessionInfo)
    
    def getProtocol(self):
        return self.protocol

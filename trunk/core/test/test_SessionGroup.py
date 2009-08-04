#!/usr/bin/python
import sys
import unittest
from SessionGroup import *
import Listener
import SessionStatus
import time
import SessionStatistics

StatusMachine = [SessionStatus.INITIAL, SessionStatus.CONNECTING, SessionStatus.RUNNING, SessionStatus.STOPPED]
class foobarListener(Listener.Listener):
    def __init__(self, object):
        self.object = object
        self.nextStatus = 0

    def onEvent(self, status, event = None):
        if status.getStatus() == SessionStatus.RUNNING:
            self.nextStatus = 3
            return
        assert status.getStatus() == StatusMachine[self.nextStatus]
        self.nextStatus = self.nextStatus + 1

address = "foobar://move"
class test_SessionGroup(unittest.TestCase):
    def setUp(self):
        self.session = SessionGroup(10,"TEST")
    
    def testCreateSession(self):
        self.session.createSession(address, 10, 1)
        assert len(self.session.connections.keys()) == 10
        self.session.createSession(address,30,20)
        assert len(self.session.connections.keys()) == 40

    def test_send_event(self):
        listener = foobarListener(self.session)
        self.session.addListener(listener)
        self.session.createSession(address, 1, 0)
        self.session.go()
        time.sleep(2)
        self.session.stop()
        time.sleep(2)

    def test_get_statictis(self):
        self.session.createSession(address, 5, 1)
        s = self.session.getStatistics()
        assert s[SessionStatus.INITIAL] == 5
        assert s[SessionStatus.RUNNING] == 0
        assert s[SessionStatus.STOPPED] == 0

        self.session.go()
        time.sleep(3)
        s = self.session.getStatistics()
        assert s[SessionStatus.RUNNING] == 5
        assert s[SessionStatus.INITIAL] == 0
        assert s[SessionStatus.STOPPED] == 0
        
        self.session.stop()
        time.sleep(4)
        s = self.session.getStatistics()
        assert s[SessionStatus.INITIAL] == 0
        assert s[SessionStatus.RUNNING] == 0
        assert s[SessionStatus.STOPPED] == 5
        
        self.session.remove()
        s = self.session.getStatistics()
        assert s[SessionStatus.INITIAL] == 0
        assert s[SessionStatus.RUNNING] == 0
        assert s[SessionStatus.STOPPED] == 0
        
    def test_remove(self):
        class listenerRemove(Listener.Listener):
            def onEvent(self,status, event = None):
                if status.getStatus() == SessionStatus.STOPPED and event == Listener.CLEAR:
                    self.receivedClearTimes += 1

            def __init__(self):
                self.receivedClearTimes = 0

        listener = listenerRemove()
        self.session.createSession(address, 2, 1)
        self.session.addListener(listener)
        self.session.go()
        time.sleep(2)
        self.session.remove()
        assert listener.receivedClearTimes == 0
        self.session.stop()
        time.sleep(2)
        self.session.remove()
        assert listener.receivedClearTimes == 2






        
        

   

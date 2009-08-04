#!/usr/bin/python
import sys
from SessionManager import *
import unittest

class test_SessionManager(unittest.TestCase):

    def setUp(self):
        self.session = SessionManager()
    
    def test_CreateSession(self):
        self.session.createSession("rtsp","foobar",2000)
        assert self.session.getSessionNumber() == 2000
        self.session.destoryAllSession()

        self.session.createSession("rtsp", "foobar",0)
        assert self.session.getSessionNumber() == 0
        self.session.createSession("rtsp","foobar",1)
        assert self.session.getSessionNumber() == 1
        

    def test_destorySession(self):
        """Create zero session"""
        self.session.createSession("rtsp", "foobar", 0)
        assert self.session.getSessionNumber() == 0
        self.session.destoryAllSession()
        assert self.session.getSessionNumber() == 0
        
        """Create 2000 sessions"""
        self.session.createSession("rtsp", "foobar",2000)
        assert self.session.getSessionNumber() == 2000
        self.session.destoryAllSession()
        assert self.session.getSessionNumber() == 0


if __name__ == "__main__":
    unittest.main()



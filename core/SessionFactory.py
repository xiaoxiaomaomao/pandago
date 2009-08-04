#!/usr/bin/python
from protocol import RTSPSessionImp
from protocol import SessionImpForTest
from protocol import RTSPSessionImpForRTP
class SessionFactory:
    @staticmethod
    def createSession(type):
        type = type.lower()
        if type == "rtsp":
            return RTSPSessionImp.RTSPSessionImp()
        
        if type == "vlc":
            return RTSPSessionImpForRTP.RTSPSessionImpForRTP()

        if type == "demo":
            return SessionImpForTest.SessionImpForTest()
        
        return None

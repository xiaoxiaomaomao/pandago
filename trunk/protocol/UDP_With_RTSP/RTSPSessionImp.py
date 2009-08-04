#!/usr/bin/python
import sys
import ctypes
import threading
import time
RTSP_PLAYER_INIT  = 0
RTSP_PLAYER_READY = 2
RTSP_PLAYER_PLAY  = 3
RTSP_PLAYER_CLOSE = 4
RTSP_PLAYER_ERROR = 5

class RTSPSessionImp():
    def __init__(self):
        self.rtsp = ctypes.CDLL("/home/sxiong/project/trunk/protocol/RTSPLIBsource/librtsp.so")
        self.handle = 0
        self.time = 0
        self.ports = "No Port"
        self.prevTime = -1
        self.detectExceptTimes = 0
        self.capture = None
        self.buffer = '0' * 2000
            
    def start(self, address, param):
        self.time = 0

        self.handle = self.rtsp.rtsp_create_handle(address)
        
        self.capture = ctypes.c_char_p(self.buffer)

        self.rtsp.rtsp_set_capture(self.handle, self.capture)
        serverceGroupId = int(param)
        ret = self.rtsp.rtsp_open(self.handle,1)
        if ret < 0:
            print "faild"
            return 
        
        ret = self.rtsp.rtsp_play(self.handle, 0)
        if ret < 0:
            print "################"
        port1 = self.rtsp.rtsp_get_ipqamport1(self.handle)
        port2 = self.rtsp.rtsp_get_ipqamport2(self.handle)
        self.ports = str(port1) + '-' + str(port2)

    def stop(self):
        self.rtsp.rtsp_close(self.handle)
        self.rtsp.rtsp_destory_client(self.handle)
    
    
    def keepAlive(self):
        ret = self.rtsp.rtsp_keepalive(self.handle)

    def getPorts(self):
        return self.ports
    
    def getPacketData(self):
        return self.capture.value
       
if __name__ == '__main__':
    rtsp = RTSPSessionImp()
    rtsp.start("rtsp://192.168.0.251/test1.ts","1");
    time.sleep(1)
    print rtsp.getPacketData()
    time.sleep(2)


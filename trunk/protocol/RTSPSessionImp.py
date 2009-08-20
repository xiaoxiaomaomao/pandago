#!/usr/bin/python
import sys
import ctypes
import threading
import time
from core import SessionImp
from core.SessionStatus import SessionStatus
import string
import os
SUCCESS = 0
FAILED = -1
RTSP_PLAYER_INIT  = 0
RTSP_PLAYER_READY = 2
RTSP_PLAYER_PLAY  = 3
RTSP_PLAYER_CLOSE = 4
RTSP_PLAYER_PAUSE = 5
RTSP_PLAYER_ERROR = 6


CONNECT_FAILED           = -100 
PLAY_SEND_FAILED         = -201
PLAY_RESPONSE_FAILED     = -202 
PLAY_CHECK_FAILED        = -300

SETUP_SEND_FAILED        = -203
SETUP_RESPONSE_FAILED    = -204
SETUP_CHECK_FAILED       = -301

PAUSE_SEND_FAILED        = -205
PAUSE_RESPONSE_FAILED    = -206
PAUSE_CHECK_FAILED       = -302

DESCRIBE_SEND_FAILED     = -207
DESCRIBE_RESPONSE_FAILED = -208
DESCRIBE_CHECK_FAILED    = -303

TEARDOWN_SEND_FAILED     = -209
TEARDOWN_RESPONSE_FAILED = -210
TEARDOWN_CHECK_FAILED    = -309

HEARTBEAT_SEND_FAILED    =  -211
HEARTBEAT_RESPONSE_FAILED = -212
HEARTBEAT_TIMEOUT        =  -213
HEARTBEAT_CHECK_FAILED   =  -214
PARAM_ERROR = -11
ErrorNoToStr = {SUCCESS: "Success",
                PARAM_ERROR: "Parameter error",
                CONNECT_FAILED: "Establish connect failed",
                PLAY_SEND_FAILED : "Play send failed",
                PLAY_RESPONSE_FAILED : "Play response failed",
                PLAY_CHECK_FAILED : "Play check failed",
                
                SETUP_SEND_FAILED : "Setup send failed",
                SETUP_RESPONSE_FAILED: "Send response failed",
                SETUP_CHECK_FAILED : "Setup check failed",
                
                PAUSE_SEND_FAILED : "Pause send failed",
                PAUSE_RESPONSE_FAILED: "Pause response failed",
                PAUSE_CHECK_FAILED: "Pause check failed",
                
                TEARDOWN_SEND_FAILED: " Tear down send failed",
                TEARDOWN_RESPONSE_FAILED: "Tear down response failed",
                TEARDOWN_CHECK_FAILED: "Tear down check failed",
                
                DESCRIBE_SEND_FAILED : "Describe send failed",
                DESCRIBE_RESPONSE_FAILED :"Describe response failed",
                DESCRIBE_CHECK_FAILED    : "Describe check failed",
                
                HEARTBEAT_SEND_FAILED: "Heart beat send failed",
                HEARTBEAT_TIMEOUT : "Heart timeout",
                HEARTBEAT_RESPONSE_FAILED : "Heart beat response failed",
                HEARTBEAT_CHECK_FAILED: "Heart beat check failed",
                }
LIBDIR = os.path.abspath(os.path.dirname(__file__))
rtspHandle = ctypes.CDLL(LIBDIR + "/UDP_With_RTSP/librtsp.so")
class RTSPSessionImp(SessionImp.SessionImp):
    EXECPTION_TIME = 20
    def __init__(self):
        global rtspHandle
        self.rtsp = rtspHandle
        self.handle = 0
        self.status = SessionStatus.INITIAL
        self.time = 0
        self.ports = "No Port"
        self.prevTime = -1
        self.detectExceptTimes = 0
        self.paramsBuffer = ctypes.create_string_buffer(512)
        self.errorCode = CONNECT_FAILED
        self.curScale = 1
        self.localPort = "No Port"

    def __initCapture(self):
        pass
    
    def __destory(self):
        self.__setErrorCodeNo()
        self.rtsp.rtsp_destory_client(self.handle)
        self.handle = 0
        
    def getErrorInfo(self):
        global ErrorNoToStr
        return  ErrorNoToStr[self.errorCode]
    
    def __setErrorCodeNo(self):
        if self.handle != 0:
            self.errorCode = self.rtsp.rtsp_get_error(self.handle)
        
    def setup(self, address, param):
        self.time = 0
        self.detectExceptTimes = 0
        self.curScale= 1
        self.status = SessionStatus.SETUP
        if type(param) != int and  param.isdigit() == False:
            self.errorCode = PARAM_ERROR
            return SessionStatus.NETWORKERROR
        
        self.handle = self.rtsp.rtsp_create_handle(address)
        if self.handle == 0:
            self.errorCode = CONNECT_FAILED;
            return SessionStatus.NETWORKERROR
        self.localPort = str(self.rtsp.rtsp_get_local_port(self.handle))
        serverceGroupId = int(param)
        ret = self.rtsp.rtsp_open(self.handle, serverceGroupId)
        if ret != SUCCESS:
            self.__destory()
            return SessionStatus.NETWORKERROR
        
        params = self.rtsp.rtsp_get_params(self.handle, self.paramsBuffer)
        
        return SessionStatus.SETUP
    
    """
    Example:
    Server: VSS/0.1.112 (Platform/Linux)\r\n
    Cseq: 2\r\n
    Session: 3712549317808461444\r\n
    Date: Fri, 27 Feb 2009 18:38:35 GMT\r\n
    Expires: Fri, 27 Feb 2009 18:38:35 GMT\r\n
    Transport: MP2T/DVBC/QAM;frequency=300000;symbol-rate=6875;modulation=3;program-number=9;destination=10.1.1.120;source=192.168.0.102;client_port=51218-51219;server_port=6970-6971
    """ 
    def __parserParam(self, transport, dic):
        string.replace(transport, '\r\n', '')
        tokens = transport.split(';')
        for token in tokens:
            result = token.split('=')
            if len(result) < 2:
                dic[result[0]] = None
            else:
                dic[result[0]] = result[1]
            
    def getParamsFromRemote(self, dict):
        self.__parserParam(self.paramsBuffer.value, dict)
    
    def __processPlayParam(self, param):
        paramDict = {'scale': 1, 'playtime': -1}
        if param == None:
            return paramDict
        
        if param.has_key('playtime'):
            paramDict['playtime'] = param['playtime']
            
        if param.has_key('scale'):
            paramDict['scale'] = param['scale']
            paramDict['playtime'] = self.time

        return paramDict
    
    def play(self, param = None):
        if self.handle == 0:
            return SessionStatus.NETWORKERROR
        
        paramDict = self.__processPlayParam(param)
        ret = self.rtsp.rtsp_play(self.handle, paramDict['playtime'], paramDict['scale'])
        self.curScale = paramDict['scale']
        if ret != SUCCESS:
            self.__destory()
            return SessionStatus.NETWORKERROR
        
        return SessionStatus.RUNNING
    
    def pause(self, param = None):
        ret = RTSP_PLAYER_ERROR
        curSessionStatus = SessionStatus.NETWORKERROR
        if self.handle != 0:
            state = self.rtsp.rtsp_get_state(self.handle)
            if state == RTSP_PLAYER_PLAY:
                curSessionStatus = SessionStatus.PAUSE
                ret = self.rtsp.rtsp_pause(self.handle)
            else:
                curSessionStatus = SessionStatus.RUNNING
                ret = self.rtsp.rtsp_play(self.handle, self.time, self.curScale)

            if ret < 0:
                self.__destory()
                return SessionStatus.NETWORKERROR
        self.status = curSessionStatus
        return curSessionStatus
    
    def stop(self, param = None):
        if self.handle != 0:
            self.rtsp.rtsp_close(self.handle) # Send TearDown
            self.rtsp.rtsp_destory_client(self.handle)
            self.handle = 0
        return SessionStatus.STOPPED
    
    def getStatus(self):
        if self.handle == 0:
            return SessionStatus.STOPPED
        
        ret = self.rtsp.rtsp_get_state(self.handle)
        
        if ret == RTSP_PLAYER_PLAY:
            if self.status == SessionStatus.EXECPTION:
                return SessionStatus.EXECPTION
            return SessionStatus.RUNNING
        
        if ret == RTSP_PLAYER_PAUSE:
            return SessionStatus.PAUSE
        
        if ret == RTSP_PLAYER_CLOSE:
            self.stop()
            return SessionStatus.STOPPED
        
        if ret == RTSP_PLAYER_INIT:
            return SessionStatus.INITIAL
        
        if ret == RTSP_PLAYER_ERROR:
            return SessionStatus.NETWORKERROR
        
        return SessionStatus.NETWORKERROR
    
    def __checkIfOccurExcept(self):
        if self.status == SessionStatus.PAUSE:
            return
        
        if self.time == self.prevTime:
            self.detectExceptTimes += 1
            if self.detectExceptTimes >= RTSPSessionImp.EXECPTION_TIME:
                self.status = SessionStatus.EXECPTION
        else:
            self.detectExceptTimes = 0
            self.prevTime = self.time
            self.status = SessionStatus.RUNNING

    def getTime(self):
        self.time = self.rtsp.rtsp_get_current_time(self.handle)
        self.__checkIfOccurExcept()
        return self.time
    
    def keepAlive(self):
        ret = self.rtsp.rtsp_keepalive(self.handle)
        if ret < 0:
            self.__setErrorCodeNo()
            return SessionStatus.NETWORKERROR
        
    def getPacketData(self):
        return "^_^ Demo IP 192.168.0.250, next version support capture packet"   

    def getLocalPort(self):
        return self.localPort

from Subject import Subject
from SessionInterface import SessionInterface
from SessionStatus import SessionStatus
from SessionAction import SessionAction
from Observer import Observer
from Monitor import Monitor
import threading
import time
class Session(Subject, SessionAction):
    def __init__(self, sessionImp, status):
        SessionAction.__init__(self)
        self.observers = []
        self.monitors = []
        self.sessionImp = sessionImp
        self.status = status
        self.lock = threading.Lock()
        self.monitorLock = threading.Lock()
        
    def init(self):
        self.notifyObserver()
        return False
        
    def stop(self, param = None):
        if self.__isAlive():
            self.sessionImp.stop()
        
        result = self.status.setStatus(SessionStatus.STOPPED)
        if result == SessionStatus.NETWORKERROR:
            status.setErrorInfo(self.sessionImp.getErrorInfo())
        self.notifyObserver()
        self.notifyMonitors()
        return True
    
    def _canStart(self):
        return self.status.getStatus() & (SessionStatus.INITIAL | SessionStatus.STOPPED | SessionStatus.NETWORKERROR);
    
    def setup(self, cmdParam = None):
        if self._canStart() == False:
            return False
        
        status = self.status
        status.setStatus(SessionStatus.CONNECTING)
        self.notifyObserver()
        time.sleep(0.1) #Delay 0.1 seconds to let the UI application display the status
        
        param = cmdParam
        if param == None:
            param = status.getParam()
 
        result = self.sessionImp.setup(status.getAddress(), param)
        status.setStatus(result)

        status.setLocalPort(self.sessionImp.getLocalPort())    

        if result == SessionStatus.NETWORKERROR:
            status.setErrorInfo(self.sessionImp.getErrorInfo())
            
        paramDict = {}
        self.sessionImp.getParamsFromRemote(paramDict)
        status.setParamsFromRemote(paramDict)
        
        status.setPacketData(None)
        status.setTime(0)
        self.notifyObserver()
        self.notifyMonitors()
        
        return False
    
    def play(self, param = None):
        ret = self.status.getStatus() & (SessionStatus.RUNNING | SessionStatus.SETUP)
        if ret == False:
            return False
        
        result = self.sessionImp.play(param)
        if result == SessionStatus.NETWORKERROR:
            self.status.setErrorInfo(self.sessionImp.getErrorInfo())
            
        self.status.setStatus(self.sessionImp.getStatus())
        self.notifyObserver()
        self.notifyMonitors()
        return False
    
    def pause(self, param = None):
        if self.__isAlive():
            result = self.sessionImp.pause(param)
            if result == SessionStatus.NETWORKERROR:
                self.status.setErrorInfo(self.sessionImp.getErrorInfo())
            self.status.setStatus(self.sessionImp.getStatus())
            
    def getStatus(self):
        return self.status
    
    def __isAlive(self):
        return self.sessionImp.getStatus() & (SessionStatus.SETUP | SessionStatus.PAUSE | SessionStatus.RUNNING | SessionStatus.EXECPTION)
        
    def updateStatus(self, param = None):
        live = self.__isAlive()
        if live:
            result = self.sessionImp.keepAlive()
            if result == SessionStatus.NETWORKERROR:
                self.status.setErrorInfo(self.sessionImp.getErrorInfo())
                
            self.status.setStatus(self.sessionImp.getStatus())
            self.status.setTime(self.sessionImp.getTime())
            self.status.setPacketData(self.sessionImp.getPacketData())
            self.notifyMonitors()
        self.notifyObserver()
        
        return live

    def remove(self, param = None):
        if self.__isAlive() == False:
            self.status.setStatus(SessionStatus.REMOVED)
            self.notifyObserver()
            return True
        return False
    
    def registerObserver(self, observer):
        self.lock.acquire()
        self.observers.append(observer)
        self.lock.release()
        
    def unregisterObserver(self, observer):
        self.lock.acquire()
        if observer in self.observers:
            self.observers.remove(observer)
        self.lock.release()
        
    def notifyObserver(self):
        self.lock.acquire()
        for observer in self.observers:
             observer.updateView(self.status)
        self.lock.release()
    
    def registerMonitor(self, monitor):
        if monitor == None:
            return 
        self.monitorLock.acquire()
        self.monitors.append(monitor)
        self.monitorLock.release()
        
    def unregisterMonitor(self, monitor):
        if monitor == None:
            return 
        self.monitorLock.acquire()
        if monitor in self.monitors:
            self.monitors.remove(monitor)
        self.monitorLock.release()
         
    def notifyMonitors(self):
        self.monitorLock.acquire()
      
        captureData = self.sessionImp.getPacketData()
        for monitor in self.monitors:
            if monitor.type == Monitor.CAPTURE_PACKET:
                self.status.setPacketData(captureData)
                filteredData = monitor.doFilter(captureData)
                self.status.setPacketData(filteredData)
                if filteredData != None:
                    monitor.updateView(filteredData)
               
            if monitor.type == Monitor.CONTROL_SESSION:
                monitor.updateView(self.status)
                
        self.monitorLock.release()
        

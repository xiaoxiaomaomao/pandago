#!/usr/bin/python
import os
APP_NAME = 'TestRobot'
APP_VERSION = '1.2'
OS_NAME = os.name

import sys
APP_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_PATH)
import thread
import time
from common import *
from core.Monitor import Monitor
from core.SessionManager import SessionManager
from core.SessionStatus import SessionStatus

Stopped = False
class TestRobot(Monitor):
    def __init__(self, manager):
        self.autorun = 0
        self.manager = manager
        self.type = Monitor.CONTROL_SESSION
        
    def updateView(self, sessionStatus):
        self.autoTestAction(sessionStatus)
    
    def autoTestAction(self, status):
        if status.getStatus() & (SessionStatus.NETWORKERROR | SessionStatus.STOPPED):
            time.sleep(0.01)
            
            self.manager.setup([status.getId()])
        if status.getStatus() == SessionStatus.SETUP:
            self.manager.play([status.getId()])
    
def startRun():
    manager.setup()
    manager.play()
    
from common.UpdateStatisticsWorker import *
import gobject
import datetime
import os
class WatchDog(UpdateInterface):

    TRY_TIMES = 4
    def __init__(self, gtkWin):
        self.tryTimes = WatchDog.TRY_TIMES
        self.gtkWin = gtkWin
        self.startTime = datetime.datetime.now()
        
    def update(self, staticstics):
        if staticstics[SessionStatus.RUNNING] == 0:
            self.tryTimes -= 1
        else:
            self.tryTimes = WatchDog.TRY_TIMES
        
        if self.tryTimes < 0:
            runTime = (datetime.datetime.now() - self.startTime).seconds
            hours = runTime / 3600
            seconds = (runTime % 3600) / 60
            info = " %d Hours %d minutes > runResult " % (hours, seconds)
            os.system("echo " +  info)
            global Stopped
            Stopped = True
            sys.exit(0)
        
def startWatchDog(manager, win):
    watchDog = WatchDog(win)
    worker = UpdateStatisticsWorker(watchDog, manager)
    worker.setScheduleTime(10)
    worker.start()

Pressure = 3
if __name__ == "__main__":
    manager = SessionManager()
    robot = TestRobot(manager)
    config = readConfigFromFile("./config.cfg")
    if config == None:
        print "please specify the  or wrong with configuration file"
        sys.exit(-1)
    
    createSession(config.protocol, 
                  config.address,
                  config.param, 
                  config.number, manager, 
                  None, TestRobot, Pressure)

    startRun()
    startWatchDog(manager, None)
    while Stopped != True:
       time.sleep(1)

    sys.exit(0)
       

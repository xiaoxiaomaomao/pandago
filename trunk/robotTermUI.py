#!/usr/bin/env python
import os
APP_NAME = 'TESTRobotWithCurses'
APP_VERSION = '1.0'
OS_NAME = os.name

import sys
APP_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_PATH)
import time
import thread
from common import *
from core.Monitor import Monitor
from core.SessionManager import SessionManager
from core.SessionStatus import SessionStatus
from ui import ui_term

Stopped = False
ALL_SESSIONS = []
ALL_SESSIONS_LOCK = thread.allocate_lock()

class TestRobot(Monitor):
    def __init__(self,manager):
        self.autorun = 0
        self.manager = manager
        self.type = Monitor.CONTROL_SESSION
    
    def updateView(self,sessionStatus):
        self.autoTestAction(sessionStatus)
    
    def autoTestAction(self,status):
        if status.getStatus() & (SessionStatus.NETWORKERROR | SessionStatus.STOPPED):
            time.sleep(0.01)
            self.manager.setup([status.getId()])
        if status.getStatus() == SessionStatus.SETUP:
            self.manager.play([status.getId()])

def startRun(manager):
    manager.setup()
    manager.play()

from common.UpdateStatisticsWorker import *
import datetime
import os

class WatchDog(UpdateInterface):
    TRY_TIMES = 4
    
    def __init__(self):
        self.tryTimes = WatchDog.TRY_TIMES
        self.startTime = datetime.datetime.now()
    
    def update(self,staticstics):
        if staticstics[SessionStatus.RUNNING] == 0:
            self.tryTimes -= 1
        else:
            self.tryTimes = WatchDog.TRY_TIMES
        
        if self.tryTimes < 0:    
            runTime = (datetime.datetime.now() - self.startTime).seconds
            hours = runTime / 3600
            seconds = (runTime % 3600) / 60
            info = "%d Hours %d minutes > runResult" % (hours,seconds)
            os.system("echo " + info)
            global Stopped
            Stopped = True
            sys.exit(0)

def startWatchDog(manager,win):
    watchDog = WatchDog()
    worker = UpdateStatisticsWorker(watchDog,manager)
    worker.setScheduleTime(10)
    worker.start()

Pressure = 3

if __name__ == '__main__':
    HELP = "run the program like: ./robot.py -u will turn on the ui,-n will run without ui"         
    ARGS = ["-h","-n"]

    try:
        manager = SessionManager()
        robot = TestRobot(manager)
        config = readConfigFromFile("./config.cfg")
        if config == None:
            print 'Error with configuration file'
            sys.exit(-1)
        if len(sys.argv) == 2:
            if sys.argv[1] == '-h':
                print HELP
                sys.exit(0)
            if sys.argv[1] == '-n':
                createSession(config.protocol, config.address, config.param, config.number, manager, None, TestRobot, Pressure)
        if len(sys.argv) == 1:
            ui = ui_term.ui_term(manager)
            ui.createView()
            createSession(config.protocol, config.address, config.param, config.number, manager, ui, TestRobot, Pressure)

        thread.start_new_thread(startRun, (manager,))
        startWatchDog(manager, None)

        while Stopped != True:
            time.sleep(10000)

    except KeyboardInterrupt:
        try:
            ui.restore_scrn()
        except NameError:
            pass
        sys.exit(1)

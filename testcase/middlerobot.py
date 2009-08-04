#!/usr/bin/python
import os
APP_NAME = 'TestRobot'
APP_VERSION = '1.2'
OS_NAME = os.name

import sys
APP_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_PATH + "/../")

import pygtk
import gtk
pygtk.require('2.0')

from ui.SessionView import SessionView
from core.SessionManager import SessionManager
from core.Monitor import Monitor
from core.SessionStatus import SessionStatus
import thread
import ConfigParser
import time
from common import *

SEEKTIME = 600
RANGE = 12
class TestRobot(Monitor):
    def __init__(self, manager):
        self.autorun = 0
        self.manager = manager
        self.type = Monitor.CONTROL_SESSION
        self.statusMachine = 0;
        self.AllActions = [
                           (self.manager.play,  {'playtime': 1900}, "Seek"),
                           (self.manager.play,  {'scale':    18},   "Trick"),
                           (self.manager.play,  {'scale':    -18},  "Trick"),
                           (self.manager.pause, "",                 "Pause"),
                           (self.manager.pause, "",                 "Play"),
                           (self.manager.play,  {'scale':0},        "Trick"),
                           (self.manager.stop,  "",                 "Stop"),
                           ]
        self.runTime = 0;

    def updateView(self, sessionStatus):
        self.autoTestAction(sessionStatus)
    
    def autoTestAction(self, status):
        id = status.getId()
        sessionStatus = status.getStatus()

        if sessionStatus == SessionStatus.NETWORKERROR:
            self.manager.setup([id])

        if sessionStatus == SessionStatus.STOPPED:
            self.statusMachine = 0
            self.runTime = 0
            self.manager.setup([id]);
        
        if sessionStatus == SessionStatus.SETUP:
            self.runTime = 0
            self.statusMachine = 0
            self.manager.play([id])
        
        if sessionStatus == SessionStatus.RUNNING:
            self.TestAction([id], status)

        if sessionStatus == SessionStatus.PAUSE:
            self.TestAction([id], status)   
    
    def TestAction(self, id, status):
        self.runTime += 1
        if self.runTime > 5:
            index  = self.statusMachine % len(self.AllActions)
            action = self.AllActions[index][0]
            param  = self.AllActions[index][1]
            infor  = self.AllActions[index][2]
            print infor + ' ' + str(param)
            action(id, param)
            self.runTime = 0
            self.statusMachine += 1
        
def destory(widget, event, data = None):
    gtk.main_quit()
    sys.exit(0)
    return False

def startRun():
    manager.setup()
    manager.play()

Pressure = 5
if __name__ == "__main__":
    manager = SessionManager()
    view = SessionView(manager)
    mainViewUI = view.createView()
    gtk.gdk.threads_init()
    robot = TestRobot(manager)
    if len(sys.argv) < 2:
        configFile = "./config.cfg"
    else:
        configFile = sys.argv[1]
    
    config = readConfigFromFile(configFile)
    if config == None:
        print "please specify the configure file"
        sys.exit(-1)
    
    createSession(config.protocol, config.address,
                   config.param, 
                   config.number, manager, 
                   view, TestRobot, Pressure)
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event", destory)
    window.add(mainViewUI)
    window.set_size_request(646,630)
    window.show_all()
    
    thread.start_new_thread(startRun, ())
   
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_level()

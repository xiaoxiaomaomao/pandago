#!/usr/bin/python
import os
APP_NAME = 'TestRobot'
APP_VERSION = '1.2'
OS_NAME = os.name

import sys
APP_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_PATH)

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

class TestRobot(Monitor):
    def __init__(self, manager):
        self.autorun = 0
        self.manager = manager
        self.type = Monitor.CONTROL_SESSION

    def updateView(self, sessionStatus):
        self.autoTestAction(sessionStatus)
    
    def autoTestAction(self, status):
        id = status.getId()
        sessionStatus = status.getStatus()

        if sessionStatus == SessionStatus.NETWORKERROR:
            self.manager.setup([id])

        if sessionStatus == SessionStatus.STOPPED:
            self.manager.setup([id]);
        
        if sessionStatus == SessionStatus.SETUP:
            self.manager.play([id])
        
        if sessionStatus == SessionStatus.RUNNING:
            pass

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
    window.set_size_request(720,630)
    window.show_all()
    
    thread.start_new_thread(startRun, ())
   
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_level()

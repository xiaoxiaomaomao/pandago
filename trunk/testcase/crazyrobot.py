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
import random
RUNNTIME = 30
RANGE = 12
ColorMap = {
            'Seek' :'\033[1;35m',
            'Pause':'\033[1;33m',
            'Stop' :'\033[1;39m',
            'Trick':'\033[1;32m',
            }

class TestRobot(Monitor):
    def __init__(self, manager):
        self.autorun = 0
        self.manager = manager
        self.type = Monitor.CONTROL_SESSION
        self.statusMachine = 0;
        self.AllActions = [

                (self.manager.play,  {'playtime':1900}, "Seek"),
                (self.manager.play,  {'playtime':89000},"Seek"),
                (self.manager.play,  {'playtime':5950}, "Seek"),
                (self.manager.play,  {'playtime':0},    "Seek"),
                (self.manager.play,  {'playtime':-500}, "Seek"),
                (self.manager.play,  {'playtime':1900}, "Seek"),
                (self.manager.play,  {'playtime':20},   "Seek"),

                (self.manager.play,  {'playtime':-190}, "Seek"),
                (self.manager.play,  {'playtime':-89},  "Seek"),
                (self.manager.play,  {'playtime':-59},  "Seek"),
                (self.manager.play,  {'playtime':0},    "Seek"),
                (self.manager.play,  {'playtime':-500}, "Seek"),
                (self.manager.play,  {'playtime':100},  "Seek"),
                (self.manager.play,  {'playtime':20},   "Seek"),

                #do Stop
                (self.manager.stop,  " ",               "Stop"),

                #Do Pause
                (self.manager.pause, " ",               "Pause"),
                (self.manager.pause, " ",               "Pause"),
                (self.manager.pause, " ",               "Pause"),
                #Do Trick
                (self.manager.play,  {'scale': -18},    "Trick"),
                (self.manager.play,  {'scale': -18},    "Trick"),
                (self.manager.play,  {'scale':-9},      "Trick"),
                (self.manager.play,  {'scale': 9},      "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':18},      "Trick"),
                (self.manager.play,  {'scale':-9},      "Trick"),
                (self.manager.play,  {'scale': 1},      "Trick"),
                (self.manager.play,  {'scale': 1},      "Trick"),
                (self.manager.play,  {'scale': 9},      "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':3443},    "Trick"),
                (self.manager.play,  {'scale':3},       "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':118},     "Trick"),
                (self.manager.play,  {'scale':-18},     "Trick"),
                (self.manager.play,  {'scale':-9},      "Trick"),
                (self.manager.play,  {'scale': 1},      "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':18},      "Trick"),
                (self.manager.play,  {'scale': 2},      "Trick"),
                (self.manager.play,  {'scale':-9},      "Trick"),
                (self.manager.play,  {'scale': 9},      "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':33},      "Trick"),
                (self.manager.play,  {'scale':3},       "Trick"),
                (self.manager.play,  {'scale':-3},      "Trick"),
                (self.manager.play,  {'scale':18},      "Trick"),
                (self.manager.play,  {'scale':-180000}, "Trick"),
                (self.manager.play,  {'scale': -33},    "Trick"),
                (self.manager.play,  {'scale': 18},     "Trick"),
                (self.manager.stop,  " ",               "Stop"),
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
            self.TestAction([id])

        if sessionStatus == SessionStatus.PAUSE:
            self.TestAction([id]) 

    def TestAction(self, id):
        self.runTime -= 1
        if self.runTime <= 0:
            numberOfAction = len(self.AllActions)
            index  = random.randint(0, numberOfAction - 1) % numberOfAction
            action = self.AllActions[index][0]
            param  = self.AllActions[index][1]
            infor  = self.AllActions[index][2]
            self.runTime = random.randint(4, RUNNTIME)
            sessionInfo = "%sID%3s  %s %s" % (ColorMap[infor],str(id), infor, str(param))
            print sessionInfo
            action(id, param)
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

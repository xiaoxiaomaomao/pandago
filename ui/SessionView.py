#!/usr/bin/python
import sys
import pygtk
import gtk
import threading
import time
from core.Observer import  Observer
from core.SessionStatus import SessionStatus
from common.UpdateStatisticsWorker import *
from ui.SessionRightKeyMenu import SessionRightKeyMenu
PROTOCOL = 0
ID = 1
STATUS = 2
TIME = 3
PARAM = 4
PORTS = 5
ADDRSS = 6
DESTINATION = 7
ERRORINFO = 8
BACKGROUND = 9

SIZE = 20


"""
    Display all session information.
"""
class SessionView(Observer, UpdateInterface):
    def __init__(self, manager):
        self.columnNames = ["Protocol","ID","Status","Time","ServiceGroup","Ports","Address", "Destination","Information"]
        
        self.statusMap = {SessionStatus.RUNNING:"Running", SessionStatus.STOPPED:"Stopped", SessionStatus.INITIAL:"Initial",\
                SessionStatus.CONNECTING:"Connecting", SessionStatus.NETWORKERROR:"Failed", SessionStatus.EXECPTION:"Execption",\
                SessionStatus.REMOVED:"Remove",\
                SessionStatus.SETUP:"Setup",
                SessionStatus.PAUSE: "Pause"}

        self.colourMap = {SessionStatus.RUNNING:"LimeGreen", SessionStatus.STOPPED:"SlateGray",\
                          SessionStatus.INITIAL:"RoyalBlue1",\
                          SessionStatus.SETUP: "YellowGreen",\
                          SessionStatus.CONNECTING:"yellow2",\
                          SessionStatus.NETWORKERROR:"red",SessionStatus.EXECPTION:"Orange",\
                          SessionStatus.REMOVED:"black",\
                          SessionStatus.PAUSE: "firebrick3"}

        
        self.listStore = None
        self.treeView = None
        self.scrollWindow = None
        self.statics = None
        
        self.runningLabel = gtk.Label("Running: 0")
        self.pauseLabel = gtk.Label("Pause: 0")
        self.stoppedLabel = gtk.Label("Stopped: 0")
        self.initialLabel = gtk.Label("Initial: 0")
        self.failingLabel = gtk.Label("Faild: 0")
        self.connectingLabel = gtk.Label("Connecting: 0")
        self.exceptionLabel = gtk.Label("Exception: 0")
        self.setupLabel = gtk.Label("Setup: 0")

        self.totalLabel = gtk.Label("Total: 0")
        self.manager = manager
        
        # accelerate finding the session in session view.
        self.accelerate = {}
        self.updateWorker = UpdateStatisticsWorker(self, manager)
        self.lock = threading.Lock()
        
        self.RightKeyMenu = SessionRightKeyMenu(manager)
         
    def __del__(self):
        self.manager.stop()
    
    def onRightMouseClick(self, widget, event, selection):
        RIGHT_BUTTON = 3
        if event.button == RIGHT_BUTTON:
            self.treeView.grab_focus()
            (model, path) = selection.get_selected_rows()
            ids = []
            for p in path:
                ids.append(model[p][ID])
            self.RightKeyMenu.createPopupMenu(self.manager, ids, event)
    
    def createView(self):
        """ protocol, id, status, time, address"""
        hBox = gtk.HBox(False, 9)
        hBox.pack_start(self.totalLabel)
        hBox.pack_start(self.setupLabel)
        hBox.pack_start(self.runningLabel)
        hBox.pack_start(self.pauseLabel)
        hBox.pack_start(self.failingLabel)
        hBox.pack_start(self.exceptionLabel)
        hBox.pack_start(self.stoppedLabel)
        hBox.pack_start(self.connectingLabel)
        hBox.pack_start(self.initialLabel)
        
        vBox = gtk.VBox()
        self.listStore = gtk.ListStore(str, int, str, int, str, str, str, str, str, str)
        self.treeView = gtk.TreeView(self.listStore)
        self.selection = self.treeView.get_selection()
        self.selection.set_mode(gtk.SELECTION_MULTIPLE)
        self.treeView.connect("button-press-event", self.onRightMouseClick, self.selection)
        i = 0
        for name in self.columnNames:
            cell = gtk.CellRendererText()
            column = gtk.TreeViewColumn(name)
            column.pack_start(cell, True)
            column.add_attribute(cell, "text", i)
            column.add_attribute(cell,"background",BACKGROUND)
            self.treeView.append_column(column)
            i = i + 1

        self.scrollWindow = gtk.ScrolledWindow()
        self.scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrollWindow.add(self.treeView)
        vBox.pack_start(self.scrollWindow,True)
        vBox.pack_start(hBox,False)
        
        self.updateWorker.start()
        return vBox

    def update(self, statics):  
        self.initialLabel.set_text("Initial: %d" % statics[SessionStatus.INITIAL])
        self.connectingLabel.set_text("Connecting: %d" % statics[SessionStatus.CONNECTING])
        self.runningLabel.set_text("Running: %d" % statics[SessionStatus.RUNNING])
        self.stoppedLabel.set_text("Stopped: %d" % statics[SessionStatus.STOPPED])
        self.failingLabel.set_text("Failing: %d" % statics[SessionStatus.NETWORKERROR])
        self.pauseLabel.set_text("Pause: %d" % statics[SessionStatus.PAUSE])
        self.exceptionLabel.set_text("Exception: %d" % statics[SessionStatus.EXECPTION])
        self.setupLabel.set_text("Setup: %d" % statics[SessionStatus.SETUP])
        total = statics.total()
        self.totalLabel.set_text("Total: %d" % total)
        
    def addNewSession(self, status):
        protocol = status.getProtocol()
        id = status.getId()
        sessionStatus = self.statusMap[status.getStatus()]
        runTime = status.getTime()
        address = status.getAddress()
        colour = self.colourMap[status.getStatus()]
        param = status.getParam()
        ports = "NoPort"
        destination = "NoAddress"
        errorInfo = ""
        iterator = self.listStore.append([protocol, id, sessionStatus, runTime, param, ports, address, destination, errorInfo,colour])
        self.accelerate[id] = iterator
        
    def __getListStoreIter(self, id):
        if self.accelerate.has_key(id) == True:
            return self.accelerate[id]
        return None
    
    def __clearStoppedSession(self,id,iterator):
        del self.accelerate[id]
        self.listStore.remove(iterator)
    
    def __setParams(self, iterator, params):
        if params.has_key('client_port'):
            self.listStore.set(iterator, PORTS, params['client_port'])
        
        if params.has_key('destination'):
            self.listStore.set(iterator, DESTINATION, params['destination'])
    
    def __setError(self, iterator, error):
        self.listStore.set(iterator, ERRORINFO, error)
        
    def updateSessionStatus(self, status):
        self.lock.acquire()
        iterator = self.__getListStoreIter(status.getId())
        if iterator != None and status.getStatus() != SessionStatus.INITIAL:
            id = self.listStore.get(iterator, ID)[0]
            if id == status.getId():
                self.listStore.set(iterator, TIME, status.getTime())
                self.listStore.set(iterator, STATUS, self.statusMap[status.getStatus()])
                
                if status.getStatus() & SessionStatus.SETUP:
                   self.__setError(iterator, "")
                   self.__setParams(iterator, status.getParamsFromRemote())
                   
                if status.getStatus() & SessionStatus.NETWORKERROR:
                    self.__setError(iterator, status.getErrorInfo())
                    
                self.listStore.set(iterator, BACKGROUND, self.colourMap[status.getStatus()])
        
        if status.getStatus() == SessionStatus.REMOVED:
            self.__clearStoppedSession(status.getId(), iterator)
            self.lock.release()
            return

        if iterator == None and status.getStatus() == SessionStatus.INITIAL:
            self.addNewSession(status)
        self.lock.release()

    #Implement the Observer interface to update the session view
    def updateView(self, status):
        self.updateSessionStatus(status)


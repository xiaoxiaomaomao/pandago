#!/usr/bin/python


import pygtk
pygtk.require('2.0')
import gtk
import SessionConfigDlg
class SessionControlPanel:
    def __add(self, widget, manager,view):
        dlg = SessionConfigDlg.SessionConfigDlg(None, manager, view)

    def __start(self, widget, manager):
        manager.setup()
        manager.play()
    
    def __stop(self, widget, manager):
        manager.stop()
    
    def __clear(self, widget,manager):
        manager.clear()
    
    def __pause(self, widget, manager):
        manager.pause()

    def __init__(self,manager,view):
        self.manager = manager
        self.addButton = gtk.Button("Add")
        self.addButton.connect("clicked",self.__add, manager, view)

        self.startButton = gtk.Button("Connect")
        self.startButton.connect("clicked", self.__start, manager)
        
        self.stopButton = gtk.Button("Stop")
        self.stopButton.connect("clicked", self.__stop, manager)
        
        self.clearButton = gtk.Button("Clear")
        self.clearButton.connect("clicked", self.__clear, manager)
        
        self.pauseButton = gtk.Button("Pause/Play")
        self.pauseButton.connect("clicked", self.__pause, manager)
        
    def createControlPanel(self):
        bbox = gtk.HButtonBox()
        bbox.set_layout(gtk.BUTTONBOX_EDGE)
        
        bbox.add(self.addButton)
        bbox.add(self.startButton)
        bbox.add(self.pauseButton)
        bbox.add(self.stopButton)
        bbox.add(self.clearButton)
        return bbox



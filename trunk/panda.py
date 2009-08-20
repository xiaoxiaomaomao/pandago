#!/usr/bin/python

import os
APP_NAME = 'Panda'
APP_VERSION = '1.6.1'
OS_NAME = os.name

import sys
APP_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_PATH)

import pygtk
import gtk
pygtk.require('2.0')

from ui.SessionView import SessionView
from ui.SessionControlPanel import SessionControlPanel
from ui.SessionConfigDlg import SessionConfigDlg
from core.SessionManager import SessionManager

class PandaUI:
    def __destory(self, widget, event, data=None):
        self.manager.forceStop()
        gtk.main_quit()
        sys.exit(0)
        return False

    def __init__(self,manager):
        self.sessionView = SessionView(manager)
        self.view = self.sessionView.createView()
        self.panel = SessionControlPanel(manager, self.sessionView).createControlPanel()
        self.manager = manager
        self.__createMainWindow()
        gtk.gdk.threads_init()

    def __createMainWindow(self):
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(self.view,True)
        vbox.pack_start(self.panel,False)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(APP_NAME + APP_VERSION)
        self.window.set_size_request(720,630)
        self.window.connect("delete_event", self.__destory)
        self.window.add(vbox)
        self.window.show_all()

    def main(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_level()
        
if __name__ == "__main__":
    manager = SessionManager()
    panda = PandaUI(manager)
    panda.main()

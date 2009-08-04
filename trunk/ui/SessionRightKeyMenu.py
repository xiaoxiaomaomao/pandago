import pygtk
import gtk
import os
from SessionMonitor import SessionMonitor
ACTION = 0
PARAM  = 1
class SessionRightKeyMenu:
    
    def __init__(self, manager):
        self.manager = manager
        self.itemsActions = { 
                        "Start" :      (self.start,  None),
                        "2X"    :      (self.doXScale, 2),
                        "3X"    :      (self.doXScale, 3),
                        "4X"    :      (self.doXScale, 4),
                        "6X"    :      (self.doXScale, 6),
                        "8X"    :      (self.doXScale, 8),
                        "9X"    :      (self.doXScale, 9),
                        "-2X"   :      (self.doXScale,-2),
                        "-3X"   :      (self.doXScale,-3),
                        "-4X"   :      (self.doXScale,-4),
                        "-6X"   :      (self.doXScale,-6),
                        "-8X"   :      (self.doXScale,-8),
                        "-9X"   :      (self.doXScale,-9), 
                        "Stop"  :      (manager.stop, None), 
                        "Pause/Play":  (manager.pause, None),
                        "Monitor"   :  (self.createMonitor, None),
                      }
        
        self.itemsName = ["Start", "2X", "3X", "4X", "6X","8X", "9X", "-2X", "-3X", "-4X", "-6X","-8X", "-9X",\
                            "Stop","Pause/Play","Monitor"]
       
    def start(self, ids, param = None):
        self.manager.setup(ids)
        self.manager.play(ids)
    
    def doXScale(self, ids, scale):
        dictParam = {'scale' : scale}
        self.manager.play(ids, dictParam)
        
    def createPopupMenu(self, manager, ids, event):
        menu = gtk.Menu()
        for name in self.itemsName:
            item = gtk.MenuItem(name)
            item.connect("activate", self.menuAction, name ,ids)
            menu.append(item)
            item.show()
        menu.popup(None, None, None, event.button, event.time)
        menu.show_all()
          
    def menuAction(self,widget, name, ids):
        action = self.itemsActions[name][ACTION]
        param  = self.itemsActions[name][PARAM]
        action(ids, param)
        
    def createMonitor(self, ids, param = None):
        if len(ids) > 0:
            monitor = SessionMonitor(self.manager, ids[0])
            self.manager.registerMonitor(monitor, ids[0])

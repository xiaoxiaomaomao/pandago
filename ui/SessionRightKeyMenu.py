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
                        "Stop"  :      (manager.stop, None), 
                        "Pause/Play":  (manager.pause, None),
                        "1X"    :      (self.doXScale, 1),
                        "3X"    :      (self.doXScale, 3),
                        "9X"    :      (self.doXScale, 9),
                        "18X"   :      (self.doXScale, 18),
                        "33X"   :      (self.doXScale, 33),
                        "-3X"   :      (self.doXScale, -3),
                        "-9X"   :      (self.doXScale, -9), 
                        "-18X"  :      (self.doXScale, -18),
                        "-33X"  :      (self.doXScale, -33),
                        "Monitor" :    (self.createMonitor, None),
                      }
        
        self.itemsName = ["Start", "Stop", "Pause/Play", "1X", "3X", "9X","18X","33X", \
                "-3X", "-9X", "-18X","-33X", "Monitor"]
       
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

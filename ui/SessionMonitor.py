import pygtk
import gtk
import os
import string
from core.Monitor import Monitor
from filter.LineFilter import LineFilter
class SessionMonitor(Monitor):
    def __destory(self, widget, event, data = None):
        self.manager.unregisterMonitor(self, self.id)

    def mouseClick(self, widget, event, treeselection):
        (model, iter) = treeselection.get_selected()
        enditer = self.textbuffer.get_end_iter()
        self.textbuffer.set_text(model.get_value(iter, 0) + '\n')
        
    def createView(self):
        self.listStore = gtk.ListStore(str,str)
        self.treeView = gtk.TreeView(self.listStore)
        self.selection = self.treeView.get_selection()
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn("packet")
        column.pack_start(cell, True)
        column.add_attribute(cell, "text", 0)
        column.add_attribute(cell,"background",1)
        self.treeView.append_column(column)
        self.selection = self.treeView.get_selection()
        self.treeView.connect("button-press-event", self.mouseClick, self.selection)
        self.scrollWindow = gtk.ScrolledWindow()
        self.scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrollWindow.add(self.treeView)
        return self.scrollWindow
        
    def __init__(self, manager, id):
        Monitor.__init__(self)
        self.color = ["CornflowerBlue","GreenYellow"]
        self.index = 0
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.__destory)
        window.set_border_width(0)
        window.set_size_request(380, 360)
        window.set_title("Monitor ID " + str(id))
        view = self.createView()
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(view, True)
      
        self.id = id
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        self.textbuffer = textview.get_buffer()
        sw.add(textview)
        sw.show()
        textview.show()
        vbox.pack_start(sw,False)
        self.manager = manager
        window.add(vbox)
        window.show_all()
        
    def updateView(self, viewData):
        enditer = self.textbuffer.get_end_iter()
        color = self.color[self.index % 2]
        self.listStore.append([viewData, color])
        self.index += 1
        
    

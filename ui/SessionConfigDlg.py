#!/usr/bin/python
import pygtk
import gtk
import os
WILDCARD = '*'
from common import *
class SessionConfigDlg:
    def __init__(self, parent, manager, view):
        self.dialog = gtk.Dialog("Configuration Session",None,gtk.DIALOG_MODAL)
        self.manager = manager
        self.view = view
        okButton = gtk.Button("OK", gtk.STOCK_OK)
        
        cancelButton = gtk.Button("Cancel", gtk.STOCK_CANCEL)

        okButton.connect("clicked", self.onButton, self)
        cancelButton.connect("clicked", self.onCancel, self)
        self.dialog.action_area.pack_start(okButton,False,False)
        self.dialog.action_area.pack_start(cancelButton, False,False)
        table = gtk.Table(5,2)
        table.set_row_spacings(5)
        table.set_col_spacings(5)
        frame = gtk.Frame("Configure")
        frame.add(table)
        
        protocolLab     = gtk.Label("Protocol :")
        addressLab      = gtk.Label("Address :")
        serviceGroupLab = gtk.Label("ServiceGroup :")
        scaleLab        = gtk.Label("Scale :")
        numberLab       = gtk.Label("Number :")
    
        hbox = gtk.HBox()
        self.singleRadio = gtk.RadioButton(None,"Individual")
        self.mutipleRadio = gtk.RadioButton(self.singleRadio,"Mutil")
        self.configureFileRadio = gtk.RadioButton(self.mutipleRadio, "Config File");
        self.configureFileRadio.connect("toggled", self.onConfigureFileRadio, self);
        self.singleRadio.set_active(True)
        
        hbox.pack_start(self.singleRadio)
        hbox.pack_start(self.mutipleRadio)
        hbox.pack_start(self.configureFileRadio)

        table.attach(protocolLab, 0, 1, 0, 1)
        table.attach(hbox,0, 2, 1, 2)
        table.attach(addressLab, 0, 1, 2, 3)
        table.attach(serviceGroupLab, 0, 1, 3, 4)
        table.attach(numberLab, 0, 1, 4, 5)
   
        
        self.combox = gtk.combo_box_new_text()
        #TODO should get the supported protocol from a configuration file.
        self.combox.append_text("RTSP")
        self.combox.append_text("VLC")
        self.combox.append_text("Demo")
        self.combox.set_active(0)

        self.address = gtk.Entry()
        self.address.set_text("rtsp://192.168.0.");
        adjustment1 = gtk.Adjustment(0, 1, 2000, 1, 0, 0)
        adjustment2 = gtk.Adjustment(0, 0, 2000, 1, 0, 0)
 
        self.number       = gtk.SpinButton(adjustment1, 0, 0)
        self.serviceGroup = gtk.SpinButton(adjustment2, 0, 0);

        table.attach(self.combox, 1, 2, 0, 1)
        table.attach(self.address, 1, 2, 2, 3)
        table.attach(self.serviceGroup ,1, 2, 3, 4)
        table.attach(self.number, 1, 2, 4, 5)
     
        self.dialog.vbox.pack_start(frame)
        self.dialog.show_all()

    def onConfigureFileRadio(self, widget, data = None):
        if widget.get_active():
            data.address.set_text("./config.cfg")
            data.serviceGroup.set_sensitive(False)
            data.number.set_sensitive(False)
        else:
            data.address.set_text("rtsp://192.168.")
            data.serviceGroup.set_sensitive(True)
            data.number.set_sensitive(True)
    
    
    def onButton(self, widget, data):
        model    = data.combox.get_model()
        index    = data.combox.get_active()
        protocol = model[index][0]
        address  = data.address.get_text()
        number   = data.number.get_value_as_int()
        serviceGroup    = data.serviceGroup.get_value_as_int()

        if data.mutipleRadio.get_active():
            createSession(protocol, address, serviceGroup, number,data.manager, self.view)
            
        if data.singleRadio.get_active():
            if address.find(WILDCARD) >= 0:
                message = "Your adddress contain a wildcard %s" % WILDCARD
                messageBox = gtk.MessageDialog(data.dialog, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE, message)
                messageBox.show_all()
                return
            createSession(protocol, address, serviceGroup, number, data.manager, self.view)
        
        if data.configureFileRadio.get_active():
            config = readConfigFromFile(address)
            if config == None:
                m = "Your configuration file have error or is nonexistent."
                messageBox = gtk.MessageDialog(data.dialog, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE, m)
                messageBox.show_all()
                return False
            createSession(config.protocol, config.address, config.param, config.number,data.manager, self.view)
        
        self.dialog.destroy()
            
    def onCancel(self, widget, data):
        self.dialog.destroy()


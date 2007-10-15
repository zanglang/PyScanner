__doc__ = """
PyScanner GUI initialization
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import gtk, gtk.glade, gobject, pygtk
from core import *
import log

scanner = Scanner()
window = None

class MainWindow:
	def __init__(self):
		#Set the Glade file
		self.gladefile = "scanner.glade"
		self.widgets = gtk.glade.XML(self.gladefile)
		
		self.widgets.signal_autoconnect({
			"on_btnClear_clicked" : self.btnClear_clicked,
			"on_menuStart_activate" : self.menuStart_activate,
			"on_menuQuit_activate" : self.menuQuit_activate,
			"on_chkLogging_toggled" : self.chkLogging_activated,
			"on_menuBluetooth_activate" : self.menuBluetooth_activate,
			"on_menuWireless_activate" : self.menuWireless_activate,
			"on_MainWindow_destroy" : self.menuQuit_activate
		})
		# pass logging window widget to logger
		log.init(self.widgets.get_widget('txtLog'))
		log.debug('MainWindow initialized')
		
		# Columns
		treeView = self.widgets.get_widget('treeView1')
		model = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
		treeView.set_model(model)
		
		#folder = { "name": 'test' }
		#iter = model.insert_before(None, None)
		#model.set_value(iter, 0, folder)
		#model.set_value(iter, 1, folder["name"])
		
		
		column = gtk.TreeViewColumn("SSID", gtk.CellRendererText(), text=1)
		treeView.append_column(column)
		
	def btnClear_clicked(self, widget):
		log.clear()
	
	def menuStart_activate(self, widget):
		if not scanner.running:
			scanner.start()
			log.debug('start')
		else:
			scanner.stop()
			log.debug('stop')
		
	def menuQuit_activate(self, widget):
		self._shutdown()
		
	def chkLogging_activated(self, widget):
		pass
	
	def menuWireless_activate(self, widget):
		pass
	
	def menuBluetooth_activate(self, widget):
		pass
	
	def _shutdown(self):
		""" Shutdown scanner """
		scanner.stop()
		log.shutdown()
		gtk.main_quit()
		
def init():
	global window
	window = MainWindow()
	
	gtk.gdk.threads_init()
	unlock()
	gtk.main()
	lock()
	
def unlock():
	gtk.gdk.threads_enter()
	
def lock():
	gtk.gdk.threads_leave()
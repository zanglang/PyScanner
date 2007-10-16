__doc__ = """
PyScanner GUI initialization
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import gtk, gtk.glade, gobject, pygtk, traceback
from core import *
import log
try:
	import hildon
	config.EnableHildon = True
except ImportError:
	config.EnableHildon = False

scanner = Scanner()
window = None

class MainWindow:
	def __init__(self):
		
		# Check for hildon bindings first
		if config.EnableHildon:
			#self.program = hildon.Program()
			#self.program.__init__()
			#self.window = hildon.Window()
			#self.window.set_title("PyScanner")
			#self.program.add_window(self.window)
			pass
		
		# Set the Glade file
		self.gladefile = "scanner.glade"
		self.widgets = gtk.glade.XML(self.gladefile)
		
		self.widgets.signal_autoconnect({
			"on_btnClear_clicked" : self.btnClear_clicked,
			"on_menuStart_activate" : self.menuStart_activate,
			"on_menuQuit_activate" : self.menuQuit_activate,
			"on_chkLogging_toggled" : self.chkLogging_activated,
			"on_menuBluetooth_activate" : self.menuBluetooth_activate,
			"on_menuWireless_activate" : self.menuWireless_activate,
			"on_MainWindow_destroy" : self.menuQuit_activate,
			"on_treeView_cursor_changed": self.treeView_changed,
			"on_menuAbout_activate" : self.menuAbout_activate,
		})
		# pass logging window widget to logger
		log.init(self.widgets.get_widget('txtLog'))
		log.debug('MainWindow initialized')
		
		# Columns
		treeView = self.widgets.get_widget('treeView1')
		model = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING,
							gobject.TYPE_STRING, gobject.TYPE_STRING,
							gobject.TYPE_STRING, gobject.TYPE_INT)
		treeView.set_model(model)
		
		treeView.append_column(
							gtk.TreeViewColumn("Name",
							gtk.CellRendererText(), text=1))
		treeView.append_column(
							gtk.TreeViewColumn("Type",
							gtk.CellRendererText(), text=2))
		treeView.append_column(
							gtk.TreeViewColumn("Chan",
							gtk.CellRendererText(), text=3))
		treeView.append_column(
							gtk.TreeViewColumn("WEP",
							gtk.CellRendererText(), text=4))
		treeView.append_column(
							gtk.TreeViewColumn("Packets",
							gtk.CellRendererText(), text=5))
		
		if config.EnableHildon:
			#menuBar = self.widgets.get_widget('menuBar')
			#newMenu = gtk.Menu()
			#for child in menuBar.get_children():
 			#	child.reparent(newMenu)
 			#self.program.set_common_menu(newMenu)
 			#menuBar.destroy()
 			pass
		
	def btnClear_clicked(self, widget):
		log.clear()
	
	def menuStart_activate(self, widget):
		if not scanner.running:
			scanner.start()
			log.debug('start')
			log.write_status('Wireless scanning started.')
		else:
			scanner.stop()
			log.debug('stop')
			log.write_status('Wireless scanning stopped.')
		
	def menuQuit_activate(self, widget):
		self._shutdown()
		
	def chkLogging_activated(self, widget):
		pass
	
	def menuWireless_activate(self, widget):
		pass
	
	def menuBluetooth_activate(self, widget):
		pass
	
	def menuAbout_activate(self, widget):
		self.widgets.get_widget('AboutDialog').show()
	
	def treeView_changed(self, widget):
		(model, iter) = self.widgets.get_widget('treeView1').get_selection().get_selected()
		if iter == None:
			return
		network = model.get_value(iter, 0)
		self.widgets.get_widget('lblSSID').set_text(network['ssid'])
		self.widgets.get_widget('lblMac').set_text(network['bssid'])
		self.widgets.get_widget('lblChannel').set_text(network['channel'])
		self.widgets.get_widget('lblEncrypt').set_text(network['wep'])
		self.widgets.get_widget('lblPackets').set_text(str(network['packets']))
		self.widgets.get_widget('lblData').set_text(network['datapackets'])
		self.widgets.get_widget('lblLLC').set_text(network['llcpackets'])
		self.widgets.get_widget('lblEncrypted').set_text(network['cryptpackets'])
		self.widgets.get_widget('lblWeak').set_text(network['weakpackets'])
		self.widgets.get_widget('lblDupe').set_text(network['dupeivpackets'])
		self.widgets.get_widget('lblDecrypted').set_text(network['decrypted'])
	
	def _shutdown(self):
		""" Shutdown scanner """
		scanner.stop()
		log.shutdown()
		gtk.main_quit()
		
def init():
	global window
	window = MainWindow()
	log.write_status('Not scanning.')
	
	gtk.gdk.threads_init()
	#unlock()
	try:
		gtk.main()
	except KeyboardInterrupt:
		window._shutdown()
	#lock()

def unlock():
	#print 'unlock'
	#traceback.print_stack()
	gtk.gdk.threads_enter()
	
def lock():
	#print 'lock'
	gtk.gdk.threads_leave()
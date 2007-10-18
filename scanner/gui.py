__doc__ = """
PyScanner GUI initialization
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import gtk, gtk.glade, gobject, os, pygtk, traceback
from core import *
import log
if config.EnableHildon:
	import hildon

scanner = Scanner()
window = None
sortOrder = gtk.SORT_ASCENDING
lastSortCol = None

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
			"on_menuLogging_activate" : self.chkLogging_toggled,
			"on_chkLogging_toggled" : self.chkLogging_toggled,
			"on_menuWireless_activate" : self.chkWireless_toggled,
			"on_chkWireless_toggled" : self.chkWireless_toggled,
			"on_menuBluetooth_activate" : self.chkBluetooth_toggled,
			"on_chkBluetooth_toggled" : self.chkBluetooth_toggled,
			"on_menuLoad_activate" : self.menuLoad_activate,
			"on_menuAnalyze_activate" : self.menuAnalyze_activate,
			"on_MainWindow_destroy" : self.menuQuit_activate,
			"on_treeView_cursor_changed": self.treeView_changed,
			"on_treeView_button_press_event": self.treeView_clicked,
			"on_menuAbout_activate" : self.menuAbout_activate
		})
		
		# pass logging window widget to logger
		log.init(self.widgets.get_widget('txtLog'))
		log.debug('MainWindow initialized')
		
		# set up preferences
		self.widgets.get_widget('menuLogging').set_active(config.EnableLogging)
		self.widgets.get_widget('chkLogging').set_active(config.EnableLogging)
		self.widgets.get_widget('menuWireless').set_active(config.EnableWireless)
		self.widgets.get_widget('chkWireless').set_active(config.EnableWireless)
		self.widgets.get_widget('menuBluetooth').set_active(config.EnableBluetooth)
		self.widgets.get_widget('chkBluetooth').set_active(config.EnableBluetooth)
		
		# Columns
		treeView = self.widgets.get_widget('treeView1')
		model = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING,
							gobject.TYPE_STRING, gobject.TYPE_STRING,
							gobject.TYPE_STRING, gobject.TYPE_INT,
							gobject.TYPE_STRING)
		treeView.set_model(model)
		
		self.add_column('Name', 1, 100)
		self.add_column('Type', 2, 40)
		self.add_column('Ch', 3, 30)
		self.add_column('WEP', 4, 40)
		self.add_column('Pkts', 5, 40)
		self.add_column('Last', 6)
		
		if config.EnableHildon:
			#menuBar = self.widgets.get_widget('menuBar')
			#newMenu = gtk.Menu()
			#for child in menuBar.get_children():
 			#	child.reparent(newMenu)
 			#self.program.set_common_menu(newMenu)
 			#menuBar.destroy()
 			pass
 		
 	def add_column(self, text, columnid, width=-1):
 		treeview = self.widgets.get_widget('treeView1')
 		column = gtk.TreeViewColumn(text, gtk.CellRendererText(), text=columnid)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_min_width(width)
		column.set_resizable(True)
		column.set_reorderable(True)
		column.set_sort_column_id(columnid)
		#column.set_clickable(True)
		#namecolumn.connect('clicked', self.row_clicked)
		treeview.append_column(column)
		#treeview.get_model().set_sort_column_id(columnid, gtk.SORT_ASCENDING)
		
	def add_network(self, network):		
		model = gui.window.widgets.get_widget('treeView1').get_model()
		bssid = network['bssid']
		if networks.has_key(bssid):
			#iter = model.get_iter(networks[bssid])
			iter = networks[bssid]
		else:
			iter = model.insert_before(None, None)
			#networks[bssid] = model.get_path(iter)
			networks[bssid] = iter
			
		model.set_value(iter, 0, network)
		model.set_value(iter, 1, network['ssid'])
		# Network type
		if network['type'].isdigit():
			network['typestr'] = kismet.NETWORK_TYPE.get(network['type'], '?')
		else:
			network['typestr'] = network['type']
			
		model.set_value(iter, 2, network['typestr'])
		model.set_value(iter, 3, network['channel'])
		# WEP
		if network['wep'].isdigit():
			code = int(network['wep'])
			network['wepstr'] = kismet.parse_wep(code)
			model.set_value(iter, 4, code > 0
						and 'Y'
						or 'N')
		else:
			network['wepstr'] = network['wep']
			model.set_value(iter, 4, network['wep'] == 'None'
						and 'N'
						or 'Y') 
		
		model.set_value(iter, 5, int(network['datasize']))
		if type(network['lasttime']) == str:
			if network['lasttime'].isdigit():
				model.set_value(iter, 6, time.strftime('%m/%d %H:%M:%S',
								time.localtime(float(network['lasttime']))))
			else:
				model.set_value(iter, 6, network['lasttime'])
		else:
			model.set_value(iter, 6, time.strftime('%m/%d %H:%M:%S', network['lasttime']))
		
	def set_text(self, widget, text):
		self.widgets.get_widget(widget).set_text(text)
	
	def btnClear_clicked(self, widget):
		log.clear()
	
	def menuStart_activate(self, widget):
		if not scanner.running:
			scanner.start()
			log.debug('start')
			log.write_status('Wireless scanning %s.' % scanner.running
							and 'started'
							or 'not started')
		else:
			scanner.stop()
			log.debug('stop')
			log.write_status('Wireless scanning %s.' % scanner.running
							and 'not stopped'
							or 'stopped')
		
	def menuQuit_activate(self, widget):
		self._shutdown()
		
	def chkLogging_toggled(self, widget):
		enable = widget.get_active()
		log.write('Logging is %s.' % (enable
									and 'enabled'
									or 'disabled'))
		config.EnableLogging = widget.get_active()
		self.widgets.get_widget('menuLogging').set_active(config.EnableLogging)
		self.widgets.get_widget('chkLogging').set_active(config.EnableLogging)
	
	def chkWireless_toggled(self, widget):
		enable = widget.get_active()
		log.write('Wireless is %s.' % (enable
									and 'enabled'
									or 'disabled'))
		config.EnableWireless = widget.get_active()
		self.widgets.get_widget('menuWireless').set_active(config.EnableWireless)
		self.widgets.get_widget('chkWireless').set_active(config.EnableWireless)
	
	def chkBluetooth_toggled(self, widget):
		enable = widget.get_active()
		log.write('Bluetooth is %s.' % (enable
									and 'enabled'
									or 'disabled'))
		config.EnableBluetooth = widget.get_active()
		self.widgets.get_widget('menuBluetooth').set_active(config.EnableBluetooth)
		self.widgets.get_widget('chkBluetooth').set_active(config.EnableBluetooth)
	
	def menuLoad_activate(self, widget):
		# locate ssid_map
		config.KismetLogPath = 'C:\\Documents and Settings\\s4089901\\Desktop\\kismet'
		
		#ssidmap = kismet.parse_ssid_map(os.path.join(config.KismetLogPath, 'ssid_map'))
		for network in kismet.load_csv(config.KismetLogPath):
			if networks.has_key(network['bssid']):
				continue
			self.add_network(network)
			
	def menuAnalyze_activate(self, widget):
		pass
	
	def menuAbout_activate(self, widget):
		self.widgets.get_widget('AboutDialog').show()
	
	def treeView_changed(self, widget):
		(model, iter) = self.widgets.get_widget('treeView1').get_selection().get_selected()
		if iter == None:
			return
		network = model.get_value(iter, 0)
		try:
			self.set_text('lblSSID', network['ssid'])
			self.set_text('lblMac', network['bssid'])
			self.set_text('lblChannel', network['channel'])
			self.set_text('lblType', network['typestr'])
			self.set_text('lblEncrypt', network['wepstr'])
			self.set_text('lblCloaked', network['cloaked'] == '1'
						and 'Yes'
						or 'No')
			self.set_text('lblPackets', network['datasize'])
			self.set_text('lblData', network['datapackets'])
			self.set_text('lblLLC', network['llcpackets'])
			self.set_text('lblEncrypted', network['cryptpackets'])
			self.set_text('lblWeak', network['weakpackets'])
			self.set_text('lblDupe', network['dupeivpackets'])
			self.set_text('lblDecrypted', network['decrypted'])
		except KeyError:
			pass
		
	def treeView_clicked(self, widget, event):
		if (event.button == 3):
			self.widgets.get_widget('PopupMenu').popup( None, None, None,
													event.button, event.time)
	
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
	unlock()
	try:
		gtk.main()
	except KeyboardInterrupt:
		window._shutdown()
	lock()

def unlock():
	#print 'unlock'
	#traceback.print_stack()
	gtk.gdk.threads_enter()
	
def lock():
	#print 'lock'
	gtk.gdk.threads_leave()
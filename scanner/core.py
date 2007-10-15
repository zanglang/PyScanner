__doc__ = """
PyScanner core
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import os, re, signal, socket, subprocess, time, threading
import gui, kismet

pattern = re.compile('\*(.*): (.*)')

class Kismet:
	def __init__(self):
		self.functions = {
			'KISMET': self.response_kismet,
			'PROTOCOLS': self.response_noop,
			'NETWORK': self.response_network,
			## Unimplemented yet
			'REMOVE': self.response_noop,
			'CLIENT': self.response_noop,
			'ALERT': self.response_noop,
			'STATUS': self.response_noop,
			'CARD': self.response_noop,
			'TIME': self.response_noop,
			'GPS': self.response_noop,
			'INFO': self.response_noop
		}
		
		#self.process = subprocess.Popen('kismet_server')
		#time.sleep(3)
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect(('localhost', 2501))
		self.sockfile = self.socket.makefile("rw")
		self.command_initialize()
		
	def loop(self):
		global pattern
		while self.socket:
			#gui.unlock()
			try:
				line = self.readline()
				#print line
				match = pattern.match(line)
				result = self.functions[match.group(1)](match.group(2))
			except EOFError:
				break
			#except KeyError:
			#	continue
			#gui.lock()
		
	def response_info(self, data):
		print data
	
	def response_kismet(self, data):
		""" *KISMET: {Version} {Start time} {Server name} {Build Revision} """
		print data
		
	def response_network(self, data):
		network = kismet.Network.parse(data)
		
		#gui.unlock()
		#model = gui.window.widgets.get_widget('treeView1').get_model()
		#iter = model.insert_before(None, None)
		#model.set_value(iter, 0, network)
		#model.set_value(iter, 1, network.bssid)
		#gui.lock()
		#print network
	
	def response_noop(self, data):
		pass
	
	def command_initialize(self):
		self.writeline('ENABLE', 'GPS lat,lon,alt,spd,heading,fix')
		self.writeline('ENABLE', 'INFO networks,packets,crypt,weak,noise,' +
					'dropped,rate,signal')
		self.writeline('ENABLE', 'REMOVE *')
		self.writeline('ENABLE', 'NETWORK bssid,type,ssid,beaconinfo,' +
					'llcpackets,datapackets,cryptpackets,weakpackets,channel,' +
					'wep,firsttime,lasttime,atype,rangeip,gpsfixed,minlat,' +
					'minlon,minalt,minspd,maxlat,maxlon,maxalt,maxspd,octets,' +
					'cloaked,beaconrate,maxrate,quality,signal,noise,' +
					'bestquality,bestsignal,bestnoise,bestlat,bestlon,bestalt,' +
					'agglat,agglon,aggalt,aggpoints,datasize,turbocellnid,' +
					'turbocellmode,turbocellsat,carrierset,maxseenrate,' +
					'encodingset,decrypted,dupeivpackets,bsstimestamp')
		self.writeline('ENABLE', 'CLIENT bssid,mac,type,firsttime,lasttime,' +
					'datapackets,cryptpackets,weakpackets,gpsfixed,minlat,' +
					'minlon,minalt,minspd,maxlat,maxlon,maxalt,maxspd,agglat,' +
					'agglon,aggalt,aggpoints,maxrate,quality,signal,noise,' +
					'bestquality,bestsignal,bestnoise,bestlat,bestlon,bestalt,' +
					'atype,ip,datasize,maxseenrate,encodingset,decrypted,wep')
		self.writeline('ENABLE', 'ALERT sec,usec,header,text')
		self.writeline('ENABLE', 'STATUS *')
		self.writeline('ENABLE', 'CARD interface,type,channel,id,' +
					'packets,hopping')
	
	def readline(self):
		str = self.sockfile.readline()
		if not str:
			raise EOFError
		if str[-2:] == '\r\n':
			str = str[:-2]
		elif str[-1:] in '\r\n':
			str = str[:-1]
		return str
	
	def writeline(self, command, options=None):
		self.socket.send('!0 ' + command + ' ' + options + '\r\n')
		
	def shutdown(self):
		self.socket.close()
		self.socket = None
		#os.kill(self.kismet.pid, signal.SIGHUP)

class Scanner:
	def __init__(self):
		self.running = False
		self.kismet = None
	
	def start(self):
		if self.running == True:
			return
		self.running = True
		self.kismet = Kismet()
		thread = threading.Thread(target=self.kismet.loop)
		thread.start()
	
	def stop(self):
		if self.running:
			self.kismet.shutdown()
		self.running = False
__doc__ = """
PyScanner core
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import os, re, signal, socket, subprocess, sys, time, threading
import config, gui, kismet, log
if config.EnableGPS:
	import gpsbt

# kismet client server protocol regex
pattern = re.compile('\*(.*): (.*)')
networks = {}
card = None

class Kismet:
	""" Main kismet server controller """
	def __init__(self):
		self.functions = {
			'KISMET': self.response_kismet,
			'NETWORK': self.response_network,
			'ALERT': self.response_alert,
			'REMOVE': self.response_remove,
			'CARD': self.response_card,
			'ERROR': self.response_error,
			## Unimplemented yet/uninteresting
			'PROTOCOLS': self.response_noop,
			'CLIENT': self.response_noop,
			'STATUS': self.response_noop,
			'TIME': self.response_noop,
			'GPS': self.response_noop,
			'INFO': self.response_noop
		}
		
		self.run_flag = True
		# Check if we need to spawn kismet server
		if config.ExecuteKismet and sys.platform != 'win32':
			self.process = subprocess.Popen('kismet_server')
			# exit critical region first
			gui.lock()
			time.sleep(5)
			gui.unlock()
			# TODO: add progress bar
		else:
			self.process = None
			
		log.write('Started kismet server')
		# connect to server
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect(('localhost', 2501))
		self.sockfile = self.socket.makefile("rw")
		log.write('Connected to kismet server')
		self.command_initialize()		
		log.write_status('Connected to kismet instance')
		
	def loop(self):
		""" Go into a loop and read from kismet """
		global pattern
		while self.run_flag:
			try:
				match = pattern.match(self.readline())
				result = self.functions[match.group(1)](match.group(2))
			except EOFError:
				break
			except Exception, e:
				print type(e), e
				gui.unlock()
				log.error('Socket error')
				gui.lock()
				break
		
	def response_info(self, data):
		""" INFO command """
		print data
	
	def response_kismet(self, data):
		""" *KISMET: {Version} {Start time} {Server name} {Build Revision} """
		print data
		
	def response_network(self, data):
		""" NETWORK information from kismet """
		gui.unlock()
		gui.window.add_network(kismet.parse(kismet.NETWORK, data))
		gui.lock()
		
	def response_card(self, data):
		""" Current wireless CARD information """
		global card
		card = kismet.parse(kismet.CARD, data)
		gui.unlock()
		log.write_status('Received %s packets on channel %s (%s)' % (card['packets'],
				card['channel'], card['hopping'] == '1' and 'hopping' or 'locked'))
		gui.lock()
		
	def response_alert(self, data):
		""" ALERT received from kismet """
		alert = kismet.parse(kismet.ALERT, data)
		gui.unlock()
		# better write it to statusbar
		log.write('Alert: ' + alert['text'])
		log.write_status('Alert: ' + alert['text'])
		gui.lock()
		
	def response_remove(self, data):
		""" REMOVE a network entry from collection. Unhandled for now """
		print 'REMOVE ' + data
		
	def response_error(self, data):
		""" kismet has detected an ERROR in protocol """
		print 'ERROR ' + data
	
	def response_noop(self, data):
		""" Do nothing """
		pass
	
	def command_initialize(self):
		""" Set up connection to kismet and send command options """
		self.writeline('ENABLE', 'NETWORK ' + ','.join(kismet.NETWORK))
		self.writeline('ENABLE', 'INFO ' + ','.join(kismet.INFO))
		#self.writeline('ENABLE', 'CLIENT ' + ','.join(kismet.CLIENT))
		self.writeline('ENABLE', 'ALERT ' + ','.join(kismet.ALERT))
		self.writeline('ENABLE', 'CARD ' + ','.join(kismet.CARD))
		self.writeline('ENABLE', 'GPS ' + ','.join(kismet.GPS))
		self.writeline('ENABLE', 'REMOVE ' + ','.join(kismet.REMOVE))
		#self.writeline('ENABLE', 'STATUS ' + ','.join(kismet.STATUS))
	
	def readline(self):
		""" Read a line of text from socket """
		str = self.sockfile.readline()
		if not str:
			raise EOFError
		if str[-2:] == '\r\n':
			str = str[:-2]
		elif str[-1:] in '\r\n':
			str = str[:-1]
		return str
	
	def writeline(self, command, options=None):
		""" Write a command to kismet """
		self.socket.send('!0 ' + command + ' ' + options + '\r\n')
		
	def shutdown(self):
		""" Prepare to close kismet and cleanup """
		self.sockfile.close()
		self.socket.close()
		self.run_flag = False
		# kill kismet if possible
		if self.process:
			try:
				os.kill(self.process.pid, signal.SIGHUP)
			except OSError, e:
				log.error('Error shutting down kismet_server')

class Scanner:
	""" Generic scanner """
	def __init__(self):
		self.running = False
		self.kismet = None
	
	def start(self):
		""" Start running """
		if self.running == True:
			return
		
		# if we are using libGPS-Bluetooth
		if config.EnableGPS:
			self.gpscontext = gpsbt.start()
			if self.gpscontext == None:
				log.error('Unable to start GPS!')
		
		# If we are scanning on wifi
		if config.EnableWireless:
			try:
				self.kismet = Kismet()
			except socket.error:
				log.error('Cannot connect to Kismet')
				return
			thread = threading.Thread(target=self.kismet.loop)
			thread.start()
		self.running = True
	
	def stop(self):
		""" Shutdown scanners """
		if self.running:
			if self.kismet.run_flag:
				self.kismet.shutdown()
			if config.EnableGPS and self.gpscontext != None:
				gpsbt.stop(self.gpscontext)
		self.running = False
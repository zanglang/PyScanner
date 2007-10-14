__doc__ = """
PyScanner core
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import os, signal, socket, subprocess, time

class Kismet:
	def __init__(self):
		self.process = subprocess.Popen('kismet_server')
		time.sleep(3)
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((localhost, 2501))
		self.sockfile = self.sock.makefile("rw")
		
	def loop(self):
		msg = ''
		while len(msg) < MSGLEN:
			chunk = self.sock.recv(MSGLEN - len(msg))
			if chunk == '':
				raise RuntimeError, "socket connection broken"
			msg += chunk
		return msg
	
	def readline(self):
		str = self.sockfile.readline()
		if not str:
			raise EOFError
		if str[-2:] == '\r\n':
			str = str[:-2]
		elif s[-1:] in '\r\n':
			str = str[:-1]
		return str
		
	def shutdown(self):
		os.kill(self.kismet.pid, signal.SIGHUP)

class Scanner:
	def __init__(self):
		self.running = False
		self.kismet = None
	
	def start(self):
		self.kismet = Kismet()
	
	def stop(self):
		if self.kismet:
			self.kismet.shutdown()
		self.kismet = None
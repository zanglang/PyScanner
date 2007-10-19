__doc__ = """
PyScanner kismet module
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import os, time

# Protocol separator
separator = '\001'

##### Protocol definitions #####
NETWORK = (
	'bssid', 'type', 'ssid',
	#'beaconinfo',
	'llcpackets', 'datapackets', 'cryptpackets', 'weakpackets', 'channel',
	'wep','cloaked','lasttime','datasize',
	#'firsttime','atype', 'rangeip', 'gpsfixed',
	#'minlat', 'minlon', 'minalt', 'minspd', 'maxlat', 'maxlon',
	#'maxalt', 'maxspd', 'octets', 'cloaked', 'beaconrate',
	#'maxrate', 'quality', 'signal', 'noise', 'bestquality',
	#'bestsignal', 'bestnoise', 'bestlat', 'bestlon', 'bestalt',
	#'agglat', 'agglon', 'aggalt', 'aggpoints',
	#'turbocellnid', 'turbocellmode', 'turbocellsat', 'carrierset',
	#'maxseenrate','encodingset',
	'decrypted','dupeivpackets'
	#,'bsstimestamp'
)

INFO = (
	'networks','packets','crypt','weak','noise',
	'dropped','rate','signal'
)

ALERT = (
	#'sec','usec',
	'header','text'
)

CARD = (
	'interface','type','channel','id','packets','hopping'
)

GPS = (
	'lat','lon','alt','spd','heading','fix'
)

REMOVE = ('*')
STATUS = ('*')

### Misc enumerations ###
NETWORK_TYPE = {
	'0': 'AP',	# access point
	'1': 'Ad-hoc',
	'2': 'Probe',
	'3': 'Turbocell',
	'4': 'Data'
}

def parse(definitions, data, store=None):
	""" Main function for parsing kismet's client/server protocol
		:param definitions: Definitions dictionary to decode the data, e.g.
			NETWORK and CARD defined in this module.
		:param store: Storage table to use (optional)"""
	# check if we are provided with a data store
	result = store and store or {}
	index = 0
	# kismet entries with spaces are enclosed in \001. Check if we need to
	# continue reading to construct a string
	continuous = False
	buffer = ''
	# split line into chunks
	for datum in data.split(' '):
		# Check separator counts. If count = 1, e.g. \001Start... or ...end\001
		# check if we were doing a continued read. Otherwise, be prepared to
		# read more chunks so we can reconstruct it.
		sepcount = datum.count(separator)
		if sepcount == 2:
			# 2 separators = self contained string. We simply need to trim them
			buffer = datum + ' '
		elif sepcount == 1:
			buffer += datum + ' '
			if continuous:
				# This should be the last chunk
				continuous = False
			else:
				continuous = True
				continue
		elif continuous:
			# No separators to end the string yet
			buffer += datum + ' '
			continue
		else:
			# separators not needed
			buffer = datum
		# Try to read the corresponding key from the definitions array.
		# Once found, use it to store our new string
		try:
			key = definitions[index]
		except IndexError:
			#print datum
			break
		result[key] = buffer.replace(separator, '')
		buffer = ''
		# move on to next string
		index += 1
		
	#print result
	return result

def parse_wep(code):
	""" Converts a kismet code to readable string form """
	wepstr = ''
	if code == 0:
		return 'None'
	if code & 0x10000:
		wepstr += 'CCMP '
	if code & 0x8000:
		wepstr += 'PPTP '
	if code & 0x4000:
		wep -= 8192
	if code & 0x2000:
		wepstr += 'PEAP '
	if code & 0x1000:
		wepstr += 'TLS '
	if code & 0x800:
		wepstr += 'TTLS '
	if code & 0x400:
		wepstr += 'LEAP '
	if code & 0x200:
		wepstr += 'AES/CCM '
	if code & 0x100:
		wepstr += 'AES/OCB '
	if code & 0x80:
		wepstr += 'PSK '
	if code & 0x40:
		wepstr += 'WPA '
	if code & 0x20:
		wepstr += 'TKIP '
	if code & 0x10:
		wepstr += 'WEP104 '
	if code & 0x8:
		wepstr += 'WEP40 '
	if code & 0x4:
		wepstr += 'Layer 3 '
	if code & 0x2:
		wepstr += 'WEP '
		
	return wepstr

def parse_ssid_map(filename):
	""" Parse kismet's ssid_map file """
	f = open(filename)
	list = None
	try:
		list = [line.split(' ', 1) for line in f.read().splitlines()]
	finally:
		f.close()
	return list

def parse_csv(filename):
	""" Parse kismet's network logs in a comma-delimited text file """
	f = open(filename)
	networks = []
	definitions = f.readline()
	# Preprocessing: it's odd Kismet writes its log files in a different
	# format than their client protocol
	definitions = definitions.replace('NetType','type')
	definitions = definitions.replace('ESSID','ssid')
	definitions = definitions.replace('Encryption','wep')
	definitions = definitions.replace('Encryption','wep')
	definitions = definitions[:-2]
	definitions = definitions.lower().split(';')
	
	for line in f:
		network = {}
		for index, item in enumerate(line.strip().split(';')):
			if item  == '': continue
			network[definitions[index]] = item
		# Post processing
		network['lasttime'] = time.strptime(network['lasttime'])
		if network['type'] == 'infrastructure':
			network['type'] = 'AP'
		else:
			network['type'] = network['type'].capitalize()
		networks.append(network)
	
	f.close()
	return networks
	
def load_csv(path):
	""" Look for kismet's network logs in path and parse them """
	networks = []
	for root, dirs, filenames in os.walk(path):
		for file in filenames:
			 filename = os.path.join(root, file)
			 if filename.endswith('.csv'):
			 	networks.extend(parse_csv(filename))
	return networks
			 
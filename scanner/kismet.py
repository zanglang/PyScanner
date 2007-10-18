import os, time

separator = '\001'

### Protocol definitions ###
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
	'1': 'Adhoc',
	'2': 'Probe',
	'3': 'Turbocell',
	'4': 'Data'
}

def parse(definitions, data, store=None):
	result = store and store or {}
	index = 0
	continuous = False
	buffer = ''
	for datum in data.split(' '):
		sepcount = datum.count(separator)
		if sepcount == 2:
			buffer = datum + ' '
		elif sepcount == 1:
			buffer += datum + ' '
			if continuous:
				continuous = False
			else:
				continuous = True
				continue
		elif continuous:
			buffer += datum + ' '
			continue
		else:
			buffer = datum
		try:
			key = definitions[index]
		except IndexError:
			#print datum
			break
		result[key] = buffer.replace(separator, '')
		buffer = ''
		index += 1
		
	#print result
	return result

def parse_wep(code):
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
	f = open(filename)
	list = None
	try:
		list = [line.split(' ', 1) for line in f.read().splitlines()]
	finally:
		f.close()
	return list

def parse_csv(filename):
	f = open(filename)
	networks = []
	definitions = f.readline()
	# Preprocessing: it's odd Kismet writes its log files in a different
	# format than their client protocol
	definitions = definitions.replace('NetType','type')
	definitions = definitions.replace('ESSID','ssid')
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
	networks = []
	for root, dirs, filenames in os.walk(path):
		for file in filenames:
			 filename = os.path.join(root, file)
			 if filename.endswith('.csv'):
			 	networks.extend(parse_csv(filename))
	return networks
			 
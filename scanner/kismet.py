import re

separator = '\001'

NETWORK = (
	'bssid', 'type', 'ssid',
	#'beaconinfo', 'llcpackets',
	'datapackets', 'cryptpackets', 'weakpackets', 'channel', 'wep',
	#'firsttime', 'lasttime', 'atype', 'rangeip', 'gpsfixed',
	#'minlat', 'minlon', 'minalt', 'minspd', 'maxlat', 'maxlon',
	#'maxalt', 'maxspd', 'octets', 'cloaked', 'beaconrate',
	#'maxrate', 'quality', 'signal', 'noise', 'bestquality',
	#'bestsignal', 'bestnoise', 'bestlat', 'bestlon', 'bestalt',
	#'agglat', 'agglon', 'aggalt', 'aggpoints', 'datasize',
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
	'sec','usec','header','text'
)

CARD = (
	'interface','type','channel','id','packets','hopping'
)

GPS = (
	'lat','lon','alt','spd','heading','fix'
)

REMOVE = ('*')
STATUS = ('*')

def parse(definitions, data):
	result = {}
	index = 0		
	continuous = False
	buffer = ''
	for datum in data.split(' '):
		sepcount = datum.count(separator)
		if sepcount == 2:
			buffer = datum
		elif sepcount == 1:
			buffer += datum
			if continuous:
				continuous = False
			else:
				continuous = True
				continue
		elif continuous:
			buffer += datum
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
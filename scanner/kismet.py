import re

separator = '\001'

class Network:
	definitions = (
				'bssid', 'type', 'ssid', 'beaconinfo', 'llcpackets',
				'datapackets', 'cryptpackets', 'weakpackets', 'channel', 'wep',
				'firsttime', 'lasttime', 'atype', 'rangeip', 'gpsfixed',
				'minlat', 'minlon', 'minalt', 'minspd', 'maxlat', 'maxlon',
				'maxalt', 'maxspd', 'octets', 'cloaked', 'beaconrate',
				'maxrate', 'quality', 'signal', 'noise', 'bestquality',
				'bestsignal', 'bestnoise', 'bestlat', 'bestlon', 'bestalt',
				'agglat', 'agglon', 'aggalt', 'aggpoints', 'datasize',
				'turbocellnid', 'turbocellmode', 'turbocellsat', 'carrierset',
				'maxseenrate','encodingset','decrypted','dupeivpackets',
				'bsstimestamp')
	@classmethod
	def parse(cls, data):
		result = {}
		index = 0		
		continuous = False
		buffer = ''
		entry = data.split(' ')
		#print entry
		for datum in entry:
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
				key = Network.definitions[index]
			except IndexError:
				print datum
			result[key] = buffer.replace(separator, '')
			buffer = ''
			#print 'key=', key, 'result=', result[key]
			index += 1
			
		#print result
		return result
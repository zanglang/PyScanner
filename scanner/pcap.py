import os
try:
	import scapy
except:
	config.EnableScapy = False
import config

def is_http(p):
	if not p.haslayer('TCP') or p.dport != 80 or not p.haslayer('Raw'):
		return False
	return p.load.startswith('GET') or p.load.startswith('POST')

def load_pcap():
	packets = scapy.PacketList()
	for root, dirs, filenames in os.walk(config.KismetPath):
		for file in filenames:
			filename = os.path.join(root, file)
			if not filename.endswith('.dump'):
				continue
			new = scapy.sniff(offline=filename, lfilter = is_http)
			# print 'new', len(new)
			packets.extend(new)
			
	print 'Summary', packets.summary()
	for p in packets:
		print p.lastlayer().name, p.load
	scapy.wrpcap('Packets.dump', packets)
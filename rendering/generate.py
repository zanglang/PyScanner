__doc__ = """
Heatmap generation script for PyScanner
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

from heatmap import Points, Renderer
import scanner.kismet, scanner.config

# A blacklist of APs known to be unencrypted / not a security issue
blacklist = ['UQconnect']

p = Points()
for network in scanner.kismet.load_csv(scanner.config.KismetPath):
	# Check if this network is considered vulnerable:
	# Filter our entries with no GPS information, non-access points and probes,
	# but keep ad-hoc networks, and also by ssid
	if network['gpsminlat'].find('90.0') >= 0 \
			or (network['type'] != 'AP' and network['type'] != 'Ad-hoc') \
			or network['ssid'] in blacklist:
		continue
	# if network has encryption, and is not using WPA or higher
	if network['wep'] != 'None' and network['wep'] != 'WEP':
		continue
	# add point diagram
	p.hit(float(network['gpsminlat']), float(network['gpsminlon']))

# process and render the diagram
r = Renderer(p)
r.process()
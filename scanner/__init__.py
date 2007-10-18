# Various sanity tests
import os.path
import config

if not os.path.exists(config.KismetPath):
	config.KismetPath = None

try:
	import gpsbt
	config.EnableGPS = True
except ImportError:
	config.EnableGPS = False
	
try:
	import hildon
	config.EnableHildon = True
except ImportError:
	config.EnableHildon = False
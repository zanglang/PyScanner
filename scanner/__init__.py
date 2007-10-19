# Various sanity tests
import os.path, sys
import config

# Test if platform supports libgps-Bluetooth
if config.EnableGPS == True:
	try:
		import gpsbt
	except ImportError:
		config.EnableGPS = False
	
# Test if platform is Hildonisable
try:
	import hildon
	config.EnableHildon = True
except ImportError:
	config.EnableHildon = False
	
# Test platform for Kismet path
if sys.platform == 'win32':
	# Uncomment and swap if necessary
	config.KismetPath = 'C:\\Documents and Settings\\s4089901\\Desktop\\kismet' 
	#config.KismetPath = os.getcwd()
if sys.platform.startswith('linux') and config.EnableHildon:
	# test for memory cards on Maemo
	if os.path.exists('/media/mmc1'):
		config.KismetPath = os.path.join('/media/mmc1', 'kismet')
	elif os.path.exists('/media/mmc2'):
		config.KismetPath = os.path.join('/media/mmc2', 'kismet')
	else:
		config.KismetPath = os.getcwd()
else:
	config.KismetPath = os.getcwd()
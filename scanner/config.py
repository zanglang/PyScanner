__doc__ = """
Scanner configuration file
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

# Enable logging messages
EnableLogging = True

# Write debug messages
LogDebug = True

# Enable wireless monitoring
EnableWireless = True

# Enable Bluetooth scanning
EnableBluetooth = False

# Enable GPS
EnableGPS = False

# Google maps database path
MapsPath = '.gmaps.db'

# GPS device address for GPSd
GpsdAddress = '/dev/rfcomm0'

#### Development flags (do not change unless necessary!) #####

# Kismet path
KismetPath = '/var/log/kismet'

# Use Hildon bindings (for Maemo)
EnableHildon = True

# Execute Kismet process
ExecuteKismet = True
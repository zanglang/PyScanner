COMS4507 - Advanced Security Project
Zhe Wei Chong - 40899013

PyScanner Notes
===============

PyScanner is designed for the Maemo platform on Nokia's N-series devices.
However, the Python code can be run in Linux and Windows just as well if
its dependencies are satisfied. For this README it is assumed that PyScanner
will be launched using a PC.


Dependencies
============
(For Ubuntu Linux)
- Python 2.5 and above
- python-pygame
- python-sqlite3
- python-gtk2
- ImageMagick
- Kismet

All of the above are directly available from Ubuntu's repository.

(For Windows)
- Python 2.5.1 for Windows (http://python.org/download/)
- PyGame (http://pygame.org/download.shtml)
- PyGTK (http://www.pygtk.org/downloads.html)
- ImageMagick (http://www.imagemagick.com/)

Running
=======
When running directly on PCs, unless running in root itself PyScanner will not
have the privileges to start or stop Kismet. It recommended to run Kismet
separately as root, and then start PyScanner normally.

To start PyScanner from the command line, cd in the main directory, and type

> python main.py

To start rendering heatmaps from Kismet's log files, type

> python rendering/generate.py

To view the heatmaps on PyMapper, type

> python rendering/GoogleMaps.py

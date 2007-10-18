import math, os, subprocess, sys, tempfile
import GoogleMaps

if sys.platform == 'win32':
	CONVERT = 'c:\\Program Files\\ImageMagick-6.3.6-Q16\\convert.exe '
else:
	CONVERT = 'convert'

class Points:
	def __init__(self):
		self.max = 0
		self.max_x = 0
		self.max_y = 0
		self.min_tilex = 0
		self.min_tiley = 0
		self.hitcount = {}
		self.hits = []
		
	def hit(self, lat, lon):
		tile, pixel = GoogleMaps.latlon2tilepixel(lat, lon, GoogleMaps.DEFAULT_ZOOM)
		if self.min_tilex == 0 or tile[0] < self.min_tilex:
			self.min_tilex = tile[0]
		if self.min_tiley == 0 or tile[1] < self.min_tiley:
			self.min_tiley = tile[1]
		self.hits.append((tile, pixel))
	
	def process(self):
		for tile, pixel in self.hits:
			x = abs(self.min_tilex - tile[0]) * 256 + pixel[0]
			y = abs(self.min_tiley - tile[1]) * 256 + pixel[1]
			if not self.hitcount.has_key((x,y)):
				self.hitcount[(x,y)] = 0
			self.hitcount[(x,y)] += 1
			self.max = max(self.max, self.hitcount[(x,y)])
			self.max_x = max(self.max_x, x)
			self.max_y = max(self.max_y, y)

class Renderer:
	def __init__(self, points):
		self.points = points
	
	def convert(self, arguments):
		process = subprocess.Popen(CONVERT + ' ' + arguments)
		process.wait()

	def normalize_spots(self):
		#intensity = 100 - math.ceil(100 / points.max)
		intensity = 30
		self.convert("%s -fill white -colorize %d%% %s" %
				(os.path.join('rendering', 'bolilla.png'),
				int(intensity), os.path.join(tempfile.gettempdir(), 'bol.png')))
	
	def iterate_points(self):
		halfwidth = 32 # dotwidth
		compose = "-page %dx%d pattern:gray100 " % \
				(self.points.max_x + halfwidth, self.points.max_y + halfwidth)
		for x, y in self.points.hitcount:
			compose += "-page +%s+%s %s " % (x - halfwidth, y - halfwidth,
					os.path.join(tempfile.gettempdir(), 'bol.png'))
	
		compose += "-background white -compose multiply -flatten %s" % \
				os.path.join(tempfile.gettempdir(), 'empty.png')
		self.convert(compose)
		
	def colorize(self):
		self.convert('%s -negate %s' %
				(os.path.join(tempfile.gettempdir(), 'empty.png'),
				os.path.join(tempfile.gettempdir(), 'full.png')))
		self.convert('%s -type TruecolorMatte %s -fx "v.p{0,u*v.h}" %s' %
				(os.path.join(tempfile.gettempdir(), 'full.png'),
				os.path.join('rendering', 'colors.png'),
				os.path.join(tempfile.gettempdir(), 'colorized.png')))
		self.convert('%s -channel A -fx "A*%f" %s' %
				(os.path.join(tempfile.gettempdir(), 'colorized.png'),
				0.5,
				'final.png'))
		
	def process(self):
		self.points.process()
		if os.path.exists('final.png'):
			print 'Removing old final.png.'
			os.remove('final.png')
		print 'Normalizing spots.'
		self.normalize_spots()
		print 'Iterating through points.'
		self.iterate_points()
		print 'Coloring the diagram.'
		self.colorize()
		print 'Done!'

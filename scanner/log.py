__doc__ = """
PyScanner core
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import config, gui, logging

if config.LogDebug:
	logging.basicConfig(level=logging.DEBUG)

logwindow = None

def init(widget):
	global logwindow
	logwindow = widget

def shutdown():
	logging.shutdown()

def debug(text):
	""" Write a debug level text """
	write('DEBUG: ' + text)

def write(text):
	""" Write text into logging window """
	buffer = logwindow.get_buffer()
	
	buffer.insert(buffer.get_end_iter(), text + '\n')
	if buffer.get_line_count() > 200:
		buffer.delete(buffer.get_start_iter(), buffer.get_iter_at_line (100))
	mark = buffer.create_mark("end", buffer.get_end_iter(), False)
	logwindow.scroll_to_mark(mark, 0.05, True, 0.0, 1.0)
	
def clear():
	""" Clear the logging window """
	buffer = logwindow.get_buffer()
	start, end = buffer.get_bounds()
	buffer.delete(start, end)
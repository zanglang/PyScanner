__doc__ = """
PyScanner logging
version 0.1 - Jerry Chong <zanglang@gmail.com>
"""

import traceback
import config, gui, logging

# is debug logging enabled?
if config.LogDebug:
	logging.basicConfig(level=logging.DEBUG)

# the textbox widget to use
logwindow = None

def init(widget):
	""" :param widget: GTK textbox widget to use for logging """
	global logwindow
	logwindow = widget

def shutdown():
	logging.shutdown()

def debug(text):
	""" Write a debug level text message """
	if not config.LogDebug:
		return
	write('DEBUG: ' + text)
	
def error(text):
	""" Write error level text message and print the stack trace """
	write('Error: ' + text)
	write(traceback.format_exc())

def write(text):
	""" Write text into logging window """
	if not config.EnableLogging:
		return
	buffer = logwindow.get_buffer()	
	buffer.insert(buffer.get_end_iter(), text + '\n')
	# delete old lines
	if buffer.get_line_count() > 200:
		buffer.delete(buffer.get_start_iter(), buffer.get_iter_at_line (100))
	mark = buffer.create_mark("end", buffer.get_end_iter(), False)
	# scroll down to last line
	logwindow.scroll_to_mark(mark, 0.05, True, 0.0, 1.0)

def write_status(text):
	""" Write text into status bar """
	gui.window.widgets.get_widget('statusBar').push(0, text)
	
def clear():
	""" Clear the logging window """
	buffer = logwindow.get_buffer()
	start, end = buffer.get_bounds()
	buffer.delete(start, end)
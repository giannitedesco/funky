import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gtk, Gdk

import cairo

from art import load_map 

def draw(self, cr):
	cr.set_source_surface(self.surf)
	cr.rectangle(0, 0, self.surf.get_width(), self.surf.get_height())
	cr.fill()

class MapView(Gtk.DrawingArea):
	def __init__(self):
		super(MapView, self).__init__()
		self.clear_map()
		self.connect('draw', draw)
		#self.set_can_focus(False)

	def clear_map(self):
		self.surf = None
		return

	def set_map(self, nr, dist):
		if not dist or nr < 0:
			self.clear_map()
			return

		p = load_map(nr)
		surf = cairo.ImageSurface(cairo.FORMAT_RGB24,
						p.get_width(),
						p.get_height())

		cr = cairo.Context(surf)

		Gdk.cairo_set_source_pixbuf(cr, p, 0, 0)
		cr.paint()

		self.surf = surf

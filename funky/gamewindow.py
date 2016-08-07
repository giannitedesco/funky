import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from art import PlantPixbufs

class PlantList(Gtk.IconView):
	def __init__(self):
		super(PlantList, self).__init__()

		s = Gtk.ListStore(Pixbuf, str)

		for plant in PlantPixbufs():
			s.append((plant, 'Plant'))
			continue

		self.set_model(s)
		self.set_pixbuf_column(0)
		self.set_text_column(1)

		self.set_spacing(0)
		self.set_row_spacing(0)
		self.set_column_spacing(0)
		self.set_item_padding(0)
		self.set_item_width(42)

class GameWindow(Gtk.Box):
	def __init__(self):
		super(GameWindow, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 6)

		self.plant_list = PlantList()

		scr = Gtk.ScrolledWindow()
		scr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scr.add(self.plant_list)

		self.pack_start(scr, True, True, 0)

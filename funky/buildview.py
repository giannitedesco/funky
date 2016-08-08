import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class BuildRow(Gtk.ListBoxRow):
	def __init__(self, bid_cb, pass_cb):
		def bid_shim(*args):
			sel = self.plants.get_selected()
			if not sel:
				return
			img, txt, idx = sel
			bid_cb(idx, self.c.get_value_as_int())
		def pass_shim(*args):
			pass_cb()
		super(BuildRow, self).__init__()

		self.add(vbox)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)


		self.plants = PlantList(indices = (-1 for x in xrange(8)))
		self.plants.set_columns(4)
		vbox.pack_start(self.plants, True, True, 5)

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		self.c = Gtk.SpinButton()
		self.c.set_range(0, 10000)
		self.c.set_numeric(True)
		self.c.set_value(1)
		self.c.set_increments(1, 1)
		p = Gtk.Button.new_with_label("pass")
		hbox.pack_start(self.c, True, True, 5)
		hbox.pack_start(b, True, True, 5)
		hbox.pack_start(p, True, True, 5)

		self.c.connect('activate', bid_shim)
		b.connect('clicked', bid_shim)
		p.connect('clicked', pass_shim)

		vbox.pack_start(hbox, False, True, 5)
		self.set_can_focus(False)

	def update_plants(self, plants):
		self.plants.update(plants)

class BuildView(Gtk.Box):
	__gsignals__ = {
		'finished-building':
			(GObject.SIGNAL_RUN_LAST, None, ()),
	}
	def __init__(self):
		def dcb(*_):
			self.emit('finished-building')

		super(BuildView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Build Cities</b>')
		done = Gtk.Button.new_with_label("Done")
		done.connect('clicked', dcb)
		self.pack_start(name, False, True, 5)
		self.pack_start(Gtk.Label('TODO: preview'), True, True, 5)
		self.pack_start(done, False, True, 5)


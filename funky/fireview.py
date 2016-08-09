import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from plantlist import PlantList

class FireBox(Gtk.Box):
	def __init__(self, plant_index, dcb):
		super(FireBox, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 0)
		self.plant_index = plant_index

		self.p = PlantList(indices = (-1, ),
					show_text = True,
					selectable = False)
		self.d = Gtk.Button.new_with_label('Demolish')
		self.f = Gtk.ToggleButton.new_with_label('Fire')

		self.d.connect('clicked', lambda x:(dcb(self.plant_index)))

		self.p.set_margin(0)

		self.pack_start(self.p, False, True, 0)
		self.pack_start(self.d, False, True, 0)
		self.pack_start(self.f, False, True, 0)

	def get_mask(self):
		if self.f.props.active:
			return 7
		else:
			return 0


class FireView(Gtk.Box):
	__gsignals__ = {
		'demolish':
			(GObject.SIGNAL_RUN_LAST, None, (int, )),
		'fire':
			(GObject.SIGNAL_RUN_LAST, None, (int, int, int, int)),
	}
	def __init__(self):
		def fcb(*_):
			self.emit('fire', *[x.get_mask() for x in self.p])

		def dcb(plant_index):
			self.emit('demolish', plant_index)

		super(FireView, self).__init__(\
				orientation = Gtk.Orientation.VERTICAL,
				spacing = 5)

		name = Gtk.Label(xalign = 0)
		name.set_markup('<b>Fire Plants</b>')
		done = Gtk.Button.new_with_label('Fire Plants')
		done.connect('clicked', fcb)

		nhb = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
					spacing = 20)
		nhb.pack_start(name, True, True, 5)

		self.p = tuple([FireBox(i, dcb) for i in xrange(4)])

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
				spacing = 5)
		for x in self.p:
			hbox.pack_start(x, True, True, 0)

		self.pack_start(nhb, False, True, 5)
		self.pack_start(hbox, True, True, 5)
		self.pack_start(done, False, True, 5)

	def update_stock(self, stock):
		for i, s in enumerate(stock):
			self.p[i].p.update_stock(0, *s)
	def update_plants(self, plants):
		for i, p in enumerate(plants):
			self.p[i].p.update_plant(0, p)
